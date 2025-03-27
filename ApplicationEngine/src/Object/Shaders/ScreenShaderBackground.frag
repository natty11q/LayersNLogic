#version 330 core

out vec4 FragColor;


in vec2 CurrentPosition;
in vec2 TextureCoordinate;

uniform sampler2D texture0;

// uniform float HudOpacity;
// uniform float Time;

// (width, Height)
// uniform vec2 Dimensions;

// (W/H)

// uniform float aspectRatio;

vec4 RenderHudTextrue()
{
    return texture(texture0,TextureCoordinate);
}


void main()
{
    FragColor = RenderHudTextrue();
    // FragColor = vec4(0.5f);
}