#version 330 core

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


vec4 RenderHudTextrue()
{
    return texture(diffuse0,TextureCoordinate) * vec4(1.0f,1.0f,1.0f,HudOpacity);
}

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

vec4 FlashCol()
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

        d = pow(0.08f/d,pow(1.1,1.1 * (Time / 10.0)));
        finalCol += col *= (d/2);
    }

    return vec4(finalCol,0.2f);
}


float sdSphere(vec3 p, float s)
{
    return length(p) - s;
}

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y,q.z)) , 0.0);
}

float smin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
}

// distance to scene
float map(vec3 p)
{
    vec3 spherePos = vec3(sin(Time)*3, 0, Time  + (sin(Time * 0.2) * 1.1));
    vec3 boxPos = vec3(sin(Time * 5)*0.09, cos(Time * 5)*0.09, 0);
    
    vec3 q = p;
    q = fract(p) - 0.5;
    
    float sphere = sdSphere(p - spherePos, 1.0);

    float box  = sdBox(q - boxPos, vec3(0.1));

    float ground = p.y + 1;

    return min(ground, smin(sphere,box,0.6));
}


vec4 mainImage()
{
    vec2 uv = ( gl_FragCoord.xy * 2.0 - Dimensions) / Dimensions.y;


    // initialise
    vec3 ro = vec3(0,0,-3 + (Time));             // ray origin
    vec3 rd = normalize(vec3(uv,1.0));  // ray direction
    vec3 col = vec3(0);

    float t = 0.0;


    // rayMarching

    for (int i = 0; i < 80; i++)
    {
        vec3 p = ro + rd * t;

        float d = map(p);

        t += d;
        
        if (d < 0.001 || t > 1000.0) break;
    }

    // col = palette(t * .04, vec3(0.9f,0.85f,0.99) ,vec3(0.5f,0.5f,0.5f) ,vec3(1.0f,1.0f,1.0f) ,vec3(0.263f, 0.416f, 0.557f));
    col = vec3(t * 0.1);
    if (col.x < 1 && t > 80) // only need to check one value when its white / grayscale
    {
        col = FlashCol().xyz * 0.2;
        // col = palette(t * .04, vec3(0.9f,0.85f,0.99) ,vec3(0.5f,0.5f,0.5f) ,vec3(1.0f,1.0f,1.0f) ,vec3(0.263f, 0.416f, 0.557f));
        // col = palette(t * .02, vec3(0.9f,0.2f,0.0f) ,vec3(0.6f,0.1f,0.2f) ,vec3(0.0f,1.0f,1.0f) ,vec3(0.563f, 0.316f, 0.057f));
    }

    // return vec4(col, 1.0f) * 0a.2;
    return vec4(col, 1.0f);
}

void main()
{
    FragColor = mainImage();
}