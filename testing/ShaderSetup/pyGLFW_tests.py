#req:  pip install glfw
#req:  pip install PyOpenGL


import glfw
from OpenGL.GL import *
import numpy as np

# Vertex Shader source code
vertex_shader_source = """
#version 330 core
layout(location = 0) in vec3 position;
void main()
{
    gl_Position = vec4(position, 1.0);
}
"""

# Fragment Shader source code
fragment_shader_source = """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        info_log = glGetShaderInfoLog(shader)
        raise RuntimeError(f"Shader compilation failed: {info_log}")
    return shader

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Set GLFW window hints (optional)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "OpenGL with GLFW", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Define the triangle vertices
    vertices = np.array([
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0
    ], dtype=np.float32)

    # Compile shaders and create shader program
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        info_log = glGetProgramInfoLog(shader_program)
        raise RuntimeError(f"Shader program linking failed: {info_log}")

    # Delete shaders as they're linked into our program now and no longer necessary
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    # Generate and bind a Vertex Array Object
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Generate and bind a Vertex Buffer Object
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Specify the layout of the vertex data
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Unbind the VBO and VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Render loop
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Render here
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw the triangle
        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    # Clean up
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)

    glfw.terminate()

if __name__ == "__main__":
    main()
