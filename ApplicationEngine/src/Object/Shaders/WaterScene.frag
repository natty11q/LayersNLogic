#version 330 core

// Render mode macros – define these if not defined externally.
#ifndef RENDER_GODRAYS
    #define RENDER_GODRAYS 1    // set to 1 to enable god-rays
#endif

#ifndef RENDER_CLOUDS
    #define RENDER_CLOUDS 1
#endif

#ifndef RENDER_WATER
    #define RENDER_WATER 1
#endif

// Uniforms provided by the OpenGL application.
uniform float iTime;         // time in seconds
uniform vec3 iResolution;    // viewport resolution (x,y,unused)
uniform sampler2D iChannel0; // texture channel for noise lookup

// Water and color parameters.
float waterlevel = 70.0;        // height of the water
float wavegain   = 1.0;         // general water wave level
float large_waveheight = 1.0;   // "heavy" waves (set to 0.0 for still ocean)
float small_waveheight = 1.0;   // small waves

vec3 fogcolor    = vec3(0.5, 0.7, 1.1);
vec3 skybottom   = vec3(0.6, 0.8, 1.2);
vec3 skytop      = vec3(0.05, 0.2, 0.5);
vec3 reflskycolor= vec3(0.025, 0.10, 0.20);
vec3 watercolor  = vec3(0.2, 0.25, 0.3);

vec3 light       = normalize(vec3(0.1, 0.25, 0.9));

// random/hash function              
float hash(float n) {
    return fract(cos(n) * 41415.92653);
}

// 2d noise function
float noise(vec2 p) {
    return textureLod(iChannel0, p * vec2(1.0/256.0), 0.0).x;
}

// 3d noise function
float noise(in vec3 x) {
    vec3 p = floor(x);
    vec3 f = smoothstep(0.0, 1.0, fract(x));
    float n = p.x + p.y * 57.0 + 113.0 * p.z;
    return mix(mix(mix(hash(n + 0.0), hash(n + 1.0), f.x),
                   mix(hash(n + 57.0), hash(n + 58.0), f.x), f.y),
               mix(mix(hash(n + 113.0), hash(n + 114.0), f.x),
                   mix(hash(n + 170.0), hash(n + 171.0), f.x), f.y), f.z);
}

mat3 m = mat3( 0.00,  1.60,  1.20,
              -1.60,  0.72, -0.96,
              -1.20, -0.96,  1.28 );

float fbm(vec3 p) {
    float f = 0.5000 * noise(p); 
    p = m * p * 1.1;
    f += 0.2500 * noise(p); 
    p = m * p * 1.2;
    f += 0.1666 * noise(p); 
    p = m * p;
    f += 0.0834 * noise(p);
    return f;
}

mat2 m2 = mat2(1.6, -1.2,
               1.2,  1.6);

float fbm(vec2 p) {
    float f = 0.5000 * noise(p); 
    p = m2 * p;
    f += 0.2500 * noise(p); 
    p = m2 * p;
    f += 0.1666 * noise(p); 
    p = m2 * p;
    f += 0.0834 * noise(p);
    return f;
}

// Calculates water height at position p.
float water(vec2 p) {
    float height = waterlevel;

    vec2 shift1 = 0.001 * vec2(iTime * 160.0 * 2.0, iTime * 120.0 * 2.0);
    vec2 shift2 = 0.001 * vec2(iTime * 190.0 * 2.0, -iTime * 130.0 * 2.0);

    float wave = 0.0;
    wave += sin(p.x * 0.021 + shift2.x) * 4.5;
    wave += sin(p.x * 0.0172 + p.y * 0.010 + shift2.x * 1.121) * 4.0;
    wave -= sin(p.x * 0.00104 + p.y * 0.005 + shift2.x * 0.121) * 4.0;
    wave += sin(p.x * 0.02221 + p.y * 0.01233 + shift2.x * 3.437) * 5.0;
    wave += sin(p.x * 0.03112 + p.y * 0.01122 + shift2.x * 4.269) * 2.5;
    wave *= large_waveheight;
    wave -= fbm(p * 0.004 - shift2 * 0.5) * small_waveheight * 24.0;

    float amp = 6.0 * small_waveheight;
    shift1 *= 0.3;
    for (int i = 0; i < 7; i++) {
        wave -= abs(sin((noise(p * 0.01 + shift1) - 0.5) * 3.14)) * amp;
        amp *= 0.51;
        shift1 *= 1.841;
        p = (m2 * p) * 0.9331;
    }
    height += wave;
    return height;
}

// Cloud intersection raycasting.
float trace_fog(in vec3 rStart, in vec3 rDirection) {
#if RENDER_CLOUDS
    vec2 shift = vec2(iTime * 80.0, iTime * 60.0);
    float sum = 0.0;
    float q2 = 0.0, q3 = 0.0;
    for (int q = 0; q < 10; q++) {
        float c = (q2 + 350.0 - rStart.y) / rDirection.y;
        vec3 cpos = rStart + c * rDirection + vec3(831.0, 321.0 + q3 - shift.x * 0.2, 1330.0 + shift.y * 3.0);
        float alpha = smoothstep(0.5, 1.0, fbm(cpos * 0.0015));
        sum += (1.0 - sum) * alpha;
        if (sum > 0.98)
            break;
        q2 += 120.0;
        q3 += 0.15;
    }
    return clamp(1.0 - sum, 0.0, 1.0);
#else
    return 1.0;
#endif
}

// Fog and water intersection function.
// It returns true if the ray intersects the water surface.
bool trace(in vec3 rStart, in vec3 rDirection, in float sundot, out float fog, out float dist) {
    float h = 20.0;
    float t = 0.0;
    float st = 1.0;
    float alpha = 0.1;
    float asum = 0.0;
    vec3 p = rStart;
    
    for (int j = 1000; j < 1120; j++) {
        if (t > 500.0)
            st = 2.0;
        else if (t > 800.0)
            st = 5.0;
        else if (t > 1000.0)
            st = 12.0;
            
        p = rStart + t * rDirection;
        
#if RENDER_GODRAYS
        if (rDirection.y > 0.0 && sundot > 0.001 && t > 400.0 && t < 2500.0) {
            alpha = sundot * clamp((p.y - waterlevel) / waterlevel, 0.0, 1.0) * st * 0.024 * smoothstep(0.80, 1.0, trace_fog(p, light));
            asum += (1.0 - asum) * alpha;
            if (asum > 0.9)
                break;
        }
#endif

        h = p.y - water(p.xz);
        
        if (h < 0.1) {
            dist = t;
            fog = asum;
            return true;
        }
        
        if (p.y > 450.0)
            break;
        
        if (rDirection.y > 0.0)
            t += 30.0 * st;
        else
            t += max(1.0, 1.0 * h) * st;
    }
    
    dist = t;
    fog = asum;
    return (h < 10.0);
}

vec3 camera(float time) {
    return vec3(500.0 * sin(1.5 + 1.57 * time), 0.0, 1200.0 * time);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 xy = -1.0 + 2.0 * fragCoord.xy / iResolution.xy;
    vec2 s = xy * vec2(1.75, 1.0);

    float time = (iTime + 13.5 + 44.0) * 0.05;
    vec3 campos = camera(time);
    vec3 camtar = camera(time + 0.4);
    campos.y = max(waterlevel + 30.0, waterlevel + 90.0 + 60.0 * sin(time * 2.0));
    camtar.y = campos.y * 0.5;

    float roll = 0.14 * sin(time * 1.2);
    vec3 cw = normalize(camtar - campos);
    vec3 cp = vec3(sin(roll), cos(roll), 0.0);
    vec3 cu = normalize(cross(cw, cp));
    vec3 cv = normalize(cross(cu, cw));
    vec3 rd = normalize(s.x * cu + s.y * cv + 1.6 * cw);

    float sundot = clamp(dot(rd, light), 0.0, 1.0);

    vec3 col;
    float fog = 0.0, dist = 0.0;
    
    if (!trace(campos, rd, sundot, fog, dist)) {
        float t = pow(1.0 - 0.7 * rd.y, 15.0);
        col = 0.8 * (skybottom * t + skytop * (1.0 - t));
        col += 0.47 * vec3(1.6, 1.4, 1.0) * pow(sundot, 350.0);
        col += 0.4 * vec3(0.8, 0.9, 1.0) * pow(sundot, 2.0);
        
#if RENDER_CLOUDS
        vec2 shift = vec2(iTime * 80.0, iTime * 60.0);
        vec4 sum = vec4(0.0);
        for (int q = 1000; q < 1100; q++) {
            float c = (float(q - 1000) * 12.0 + 350.0 - campos.y) / rd.y;
            vec3 cpos = campos + c * rd + vec3(831.0, 321.0 + float(q - 1000) * 0.15 - shift.x * 0.2, 1330.0 + shift.y * 3.0);
            float alpha = smoothstep(0.5, 1.0, fbm(cpos * 0.0015)) * 0.9;
            vec3 localcolor = mix(vec3(1.1, 1.05, 1.0), 0.7 * vec3(0.4, 0.4, 0.3), alpha);
            alpha = (1.0 - sum.w) * alpha;
            sum += vec4(localcolor * alpha, alpha);
            if (sum.w > 0.98)
                break;
        }
        float alpha = smoothstep(0.7, 1.0, sum.w);
        sum.rgb /= (sum.w + 0.0001);
        sum.rgb -= 0.6 * vec3(0.8, 0.75, 0.7) * pow(sundot, 13.0) * alpha;
        sum.rgb += 0.2 * vec3(1.3, 1.2, 1.0) * pow(sundot, 5.0) * (1.0 - alpha);
        col = mix(col, sum.rgb, sum.w * (1.0 - t));
#endif

        col += vec3(0.5, 0.4, 0.3) * fog;
    } else {
#if RENDER_WATER
        vec3 wpos = campos + dist * rd;
        vec2 xdiff = vec2(0.1, 0.0) * wavegain * 4.0;
        vec2 ydiff = vec2(0.0, 0.1) * wavegain * 4.0;
        rd = reflect(rd, normalize(vec3(water(wpos.xz - xdiff) - water(wpos.xz + xdiff), 1.0, water(wpos.xz - ydiff) - water(wpos.xz + ydiff))));
        float refl = 1.0 - clamp(dot(rd, vec3(0.0, 1.0, 0.0)), 0.0, 1.0);
        float sh = smoothstep(0.2, 1.0, trace_fog(wpos + 20.0 * rd, rd)) * 0.7 + 0.3;
        float wsky = refl * sh;
        float wwater = (1.0 - refl) * sh;
        float sundot = clamp(dot(rd, light), 0.0, 1.0);
        col = wsky * reflskycolor;
        col += wwater * watercolor;
        col += vec3(0.003, 0.005, 0.005) * (wpos.y - waterlevel + 30.0);
        float wsunrefl = wsky * (0.5 * pow(sundot, 10.0) + 0.25 * pow(sundot, 3.5) + 0.75 * pow(sundot, 300.0));
        col += vec3(1.5, 1.3, 1.0) * wsunrefl;
#endif

        float fo = 1.0 - exp(-pow(0.0003 * dist, 1.5));
        vec3 fco = fogcolor + 0.6 * vec3(0.6, 0.5, 0.4) * pow(sundot, 4.0);
        col = mix(col, fco, fo);
        col += vec3(0.5, 0.4, 0.3) * fog;
    }

    fragColor = vec4(col, 1.0);
}

out vec4 FragColor;

void main() {
    mainImage(FragColor, gl_FragCoord.xy);
}
