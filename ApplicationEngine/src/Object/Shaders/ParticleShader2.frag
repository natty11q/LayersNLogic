#version 330 core

// Uniforms
out vec4 FragColor;


in vec2 CurrentPosition;
in vec2 TextureCoordinate;

uniform sampler2D diffuse0;
uniform float HudOpacity;
uniform float Time;

// (width, Height)
uniform vec2 Dimensions;

// (W/H)
uniform float aspectRatio;

uniform vec2 Campos_XY;
// Random function
float rand(vec2 co) {
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453123);
}

// Particle function
vec4 particle(vec2 uv, float id, float speed) {
    float xOffset = rand(vec2(id, 1.0)) * 2.0 - 1.0;  // Random horizontal offset
    float size = mix(0.002, 0.02, rand(vec2(id, 2.0))); // Size variation
    float heightOffset = mod(Time * speed + rand(vec2(id, 3.0)) * 5.0, 2.0) - 1.0;
    
    vec2 pos = vec2(xOffset, heightOffset);
    float dist = length(uv - pos);

    // Opacity based on distance to particle center
    float alpha = smoothstep(size, size * 0.5, dist);

    // Color gradient from blue to white
    vec3 color = mix(vec3(0.2, 0.4, 1.0), vec3(1.0), dist / size);

    return vec4(color, alpha); // Return color with alpha transparency
}

void main() {
    vec2 uv = (gl_FragCoord.xy / Dimensions) * 2.0 - 1.0; // Normalize to [-1,1]
    uv.x *= Dimensions.x / Dimensions.y; // Aspect correction

    vec3 finalColor = vec3(0.0);
    float finalAlpha = 0.0;

    // Render multiple particles
    for (int i = 0; i < 20; i++) {
        float speed = mix(0.2, 1.0, rand(vec2(i, 5.0))); // Closer particles move faster
        vec4 particleColor = particle(uv, float(i), speed);
        
        // Blend particles additively
        finalColor += particleColor.rgb * particleColor.a;
        finalAlpha += particleColor.a;
    }

    // Ensure alpha does not exceed 1.0 (to avoid over-brightness)
    finalAlpha = clamp(finalAlpha, 0.0, 1.0);
    
    FragColor = vec4(finalColor, finalAlpha);
}
