#version 330 core

out vec4 FragColor;


in vec2 CurrentPosition;
in vec2 TextureCoordinate;

uniform sampler2D texture0;
uniform float HudOpacity;
uniform float Time;

// (width, Height)
uniform vec2 Dimensions;

// (W/H)
uniform float aspectRatio;

vec4 RenderHudTextrue()
{
    return texture(texture0,TextureCoordinate) * vec4(1.0f,1.0f,1.0f,HudOpacity);
}

// struct uiButton
// {
//     bool isDown;
// };

vec4 TestingRender()
{
    vec4 DisplayOutput;

    if (true)
    {

    }


    return DisplayOutput;
}

float clamp(float x, float lowerlimit, float upperlimit) {
    if (x < lowerlimit) return lowerlimit;
    if (x > upperlimit) return upperlimit;
    return x;
}

float smoothstep(float x, float edge0, float edge1)
{
    x = clamp((x - edge0) / (edge1 - edge0) , 0.0f ,  1.0f);
    return x * x * (3.0f - 2.0f * x);
}

float step(float value,float thresh)
{
    return float(value >= thresh);
}



vec3 palette(float t , vec3 a , vec3 b , vec3 c , vec3 d)
{
    return a + b * cos(6.28318f* (c*t+d) );
}

void main()
{

    vec2 UV = ( gl_FragCoord.xy / Dimensions ) * 2.0f - 1.0f;
    UV.x *= aspectRatio; // Fix Aspect Ratio

    vec2 UV0 = UV;
    vec3 finalCol = vec3(0.0f);

    

    for (float i = 0.0f ; i < 5.0f; i++)
    {
        UV *= 1.5f;
        UV = fract(UV*1.1);
        UV -= 0.5f;

        float d = length(UV) * exp(-length(UV0)) * 4.0f * Time/3000.0f;
        
        vec3 col = palette(length(UV0) + i * 0.6f + Time * 0.2f, vec3(0.5f,0.5f,0.5f) ,vec3(0.5f,0.5f,0.5f) ,vec3(1.0f,1.0f,1.0f) ,vec3(0.263f, 0.416f, 0.557f) );
        
        d = sin(d*10.0f + 2*Time)/12.0f;
        d = abs(d);

        // d = step(0.1, d);
        d = smoothstep(d , 0.0f, 0.14f);

        d = pow(0.08f/d,pow(1.1,1.1 * (Time / 1000.0)));
        finalCol += col *= (d/2);
    }

    FragColor = vec4(finalCol,0.2f);
}