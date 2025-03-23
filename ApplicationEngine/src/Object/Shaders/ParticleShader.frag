#version 330 core

out vec4 FragColor;

in vec2 CurrentPosition;
in vec2 TextureCoordinate;

// uniform sampler2D diffuse0;
uniform float HudOpacity;
uniform float Time;

// (width, Height)
uniform vec2 Dimensions;

// (W/H) aspect ratio
uniform float aspectRatio;

uniform vec2 Campos_XY;

// vec4 RenderHudTexture() {
//     // Render the HUD texture with the given opacity
//     return texture(diffuse0, TextureCoordinate) * vec4(1.0f, 1.0f, 1.0f, HudOpacity);
// }

// Utility functions

float clamp(float x, float lowerLimit, float upperLimit) {
    return max(lowerLimit, min(x, upperLimit));
}

float smoothstep(float x, float edge0, float edge1) {
    x = clamp((x - edge0) / (edge1 - edge0), 0.0f, 1.0f);
    return x * x * (3.0f - 2.0f * x);
}

vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    // Generate a color palette based on the input parameters
    return a + b * cos(6.28318 * (c * t + d));
}

vec4 FlashCol() {
    // Normalize UV coordinates and adjust for aspect ratio
    vec2 UV = (gl_FragCoord.xy / Dimensions) * 2.0f - 1.0f;
    UV.x *= aspectRatio;

    vec2 UV0 = UV;
    vec3 finalCol = vec3(0.0f);

    // Iterate to create a flashing effect
    for (float i = 0.0f; i < 5.0f; i++) {
        UV *= 1.5f;
        UV = fract(UV * 1.1);
        UV -= 0.5f;

        float d = length(UV) * exp(-length(UV0)) * 4.0f * Time / 3000.0f;

        // Generate the color for this iteration
        vec3 col = palette(length(UV0) + i * 0.6f + Time * 0.2f, vec3(0.5f, 0.5f, 0.5f), vec3(0.5f, 0.5f, 0.5f), vec3(1.0f, 1.0f, 1.0f), vec3(0.263f, 0.416f, 0.557f));
        
        d = sin(d * 10.0f + 2 * Time) / 12.0f;
        d = abs(d);

        d = smoothstep(d, 0.0f, 0.14f);
        d = pow(0.08f / d, pow(1.1, 1.1 * (Time / 10.0)));
        
        // Accumulate the final color
        finalCol += col * (d / 2);
    }

    return vec4(finalCol, 0.2f);
}

// Particle system effect
vec4 ParticleEffect(vec2 uv) {
    // Particle size and movement based on time
    float size = 0.05f + 0.03f * sin(Time * 0.5f + uv.x * 10.0f);
    float speed = 0.02f + 0.01f * cos(Time + uv.y * 10.0f);
    
    // Random color variation based on time and position
    vec3 particleColor = palette(mod(uv.x + Time * 0.1f, 1.0f), vec3(0.8f, 0.2f, 0.0f), vec3(0.1f, 0.3f, 0.8f), vec3(0.5f, 0.5f, 0.5f), vec3(0.7f, 0.2f, 0.1f));

    // Adjust transparency based on particle movement and time
    float opacity = smoothstep(0.2f, 0.3f, abs(sin(Time * 0.2f + uv.x * 2.0f)));

    // Create the final particle effect by mixing the size, speed, and color
    return vec4(particleColor * speed, opacity);
}

void main() {
    vec2 uv = (gl_FragCoord.xy * 2.0f - Dimensions) / Dimensions.y;

    // // Apply the particle effect
    vec4 particle = ParticleEffect(uv);

    // // Optionally add HUD texture if desired
    // if (HudOpacity > 0.0f) {
    //     vec4 hud = RenderHudTexture();
    //     FragColor = mix(hud, particle, HudOpacity);
    // } else {
    // }
    FragColor = particle;
}
