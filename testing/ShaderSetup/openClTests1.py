import pyopencl as cl
import numpy as np

# Set up an OpenCL context and command queue.
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# --- OpenCL kernel code ---
# The vertex shader kernel takes input 2D vertices and multiplies them by a 2x2 uniform matrix.
vertex_shader_source = """
__kernel void vertex_shader(
    __global const float2 *in_vertices,
    __global float2 *out_vertices,
    __constant float2 *uniform_matrix  // uniform_matrix[0] = (a, b), uniform_matrix[1] = (c, d)
){
    int i = get_global_id(0);
    float2 v = in_vertices[i];
    float2 m0 = uniform_matrix[0];
    float2 m1 = uniform_matrix[1];
    float2 transformed = (float2)(v.x * m0.x + v.y * m1.x,
                                  v.x * m0.y + v.y * m1.y);
    out_vertices[i] = transformed;
}
"""

# The fragment shader kernel takes input RGB colors and multiplies each by a uniform brightness factor.
fragment_shader_source = """
__kernel void fragment_shader(
    __global const float3 *in_colors,
    __global float3 *out_colors,
    const float brightness  // uniform brightness value
){
    int i = get_global_id(0);
    float3 col = in_colors[i];
    out_colors[i] = col * brightness;
}
"""

# Combine kernels into a single OpenCL program.
program_source = vertex_shader_source + "\n" + fragment_shader_source
program = cl.Program(ctx, program_source).build()

# --- Vertex shader stage ---
# Define some 2D vertices. (For example, a triangle.)
vertices = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [0.0, 1.0]
], dtype=np.float32)

# We'll output the transformed vertices here.
out_vertices = np.empty_like(vertices)

# Define a uniform 2x2 transformation matrix.
# For instance, a scaling matrix that doubles each coordinate.
uniform_matrix = np.array([
    [2.0, 0.0],
    [0.0, 2.0]
], dtype=np.float32)

# Create OpenCL buffers for vertex data and the uniform.
mf = cl.mem_flags
in_vert_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=vertices)
out_vert_buf = cl.Buffer(ctx, mf.WRITE_ONLY, out_vertices.nbytes)
# Note: We flatten the 2x2 matrix as two float2 values.
uniform_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=uniform_matrix.flatten())

# Set up and run the vertex shader kernel.
vertex_shader_kernel = program.vertex_shader
vertex_shader_kernel.set_args(in_vert_buf, out_vert_buf, uniform_buf)
cl.enqueue_nd_range_kernel(queue, vertex_shader_kernel, (vertices.shape[0],), None)
cl.enqueue_copy(queue, out_vertices, out_vert_buf)
queue.finish()

print("Transformed vertices:")
print(out_vertices)

# --- Fragment shader stage ---
# Define input colors (one per vertex) as RGB float3 values.
colors = np.array([
    [1.0, 0.0, 0.0],  # Red
    [0.0, 1.0, 0.0],  # Green
    [0.0, 0.0, 1.0]   # Blue
], dtype=np.float32)

out_colors = np.empty_like(colors)
brightness = np.float32(0.5)  # Reduce brightness by half.

# Create buffers for color data.
in_color_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=colors)
out_color_buf = cl.Buffer(ctx, mf.WRITE_ONLY, out_colors.nbytes)

# Set up and run the fragment shader kernel.
fragment_shader_kernel = program.fragment_shader
fragment_shader_kernel.set_args(in_color_buf, out_color_buf, brightness)
cl.enqueue_nd_range_kernel(queue, fragment_shader_kernel, (colors.shape[0],), None)
cl.enqueue_copy(queue, out_colors, out_color_buf)
queue.finish()

print("Modified colors:")
print(out_colors)
