#version 330 core

// Output color.
out vec4 FragColor;

// Varying inputs (e.g., passed from the vertex shader).
in vec2 CurrentPosition;
in vec2 TextureCoordinate;

// Uniforms.
uniform float Time;
uniform vec2 Dimensions;    // Screen (width, height)
uniform float aspectRatio;  // width / height

const float PI = 3.14159265;

// ------------------------------------------------------------
// A simple pseudo-noise function (for 3D coordinates).
float pseudoNoise(vec3 p) {
    return fract(sin(dot(p, vec3(12.9898, 78.233, 37.719))) * 43758.5453);
}

// Fractal Brownian Motion (fBM) to create turbulence.
float fBM(vec3 p) {
    float total = 0.0;
    float amplitude = 1.0;
    float frequency = 1.0;
    for (int i = 0; i < 4; i++) {
        total += amplitude * pseudoNoise(p * frequency);
        amplitude *= 0.5;
        frequency *= 2.0;
    }
    return total;
}

// Mapping function: returns a density value based on position.
float map(vec3 p) {
    float noiseVal = fBM(p);
    // Adjust scaling to control density.
    return clamp(noiseVal * 0.8, 0.0, 1.0);
}

// Raymarching function to accumulate density along a ray.
vec4 raymarch(vec3 ro, vec3 rd) {
    float t = 0.0;
    vec4 colAccum = vec4(0.0);
    const int MAX_STEPS = 100;
    
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 pos = ro + t * rd;
        float density = map(pos);
        
        if (density > 0.01) {
            vec4 sample = vec4(vec3(1.0), density);
            // Front-to-back compositing.
            colAccum.rgb += sample.rgb * sample.a * (1.0 - colAccum.a);
            colAccum.a += sample.a * (1.0 - colAccum.a);
            if (colAccum.a > 0.95)
                break;
        }
        
        t += 0.05;
        if (t > 20.0)
            break;
    }
    
    return clamp(colAccum, 0.0, 1.0);
}

void main() {
    // // Convert CurrentPosition to normalized device coordinates.
    // vec2 uv = (CurrentPosition / Dimensions) * 2.0 - 1.0;
    // uv.x *= aspectRatio; // Correct for aspect ratio.
    
    // // Set up a basic camera.
    // // Here we use a fixed XY origin (0,0) and animate the Z component over time.
    // vec3 ro = vec3(0.0, 0.0, -3.0 + Time * 0.1);
    // // Create a ray direction from the camera through the pixel.
    // vec3 rd = normalize(vec3(uv, 1.0));
    
    // // Perform raymarching to compute a volumetric (cloud-like) effect.
    // vec4 cloudColor = raymarch(ro, rd);
    
    // // Define a simple background sky color.
    // vec3 skyColor = vec3(0.6, 0.8, 1.0);
    // // Composite the clouds over the sky.
    // vec3 finalColor = mix(skyColor, cloudColor.rgb, cloudColor.a);
    
    FragColor = vec4(0.2 * (CurrentPosition.y / 2) ,0.3 * (CurrentPosition.y / 2),0.7 + (CurrentPosition.y * .3), 1.0);
}
