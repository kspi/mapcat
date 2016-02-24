#define M_PI 3.1415926535897932384626433832795
#define GOLDEN_RATIO ((1 + sqrt(5)) / 2)

uniform float width;
uniform float freq;
uniform int frame;
uniform int fps;
uniform float duration;
uniform sampler2D texture;
varying vec2 v_texcoord;


float t = float(frame) / float(fps);
float period = 8 - 4 * pow(t / duration, 1.4);
float turn = 3 * t / period;
float zoom = -t / period;
float scale = 0.55 + 0.25 * pow(t / duration, 1.8);

vec2 polar(vec2 p) {
    p = p * 2 - 1; // center
    return vec2(atan(p.y, p.x), length(p));
}

vec2 spiral(vec2 p) {
    p = polar(p);
    float phi = p.x;
    float r = p.y;

    phi /= 2 * M_PI;

    r = scale * log(scale * r) / log(GOLDEN_RATIO);
    r = 1 - r;
    r = r + 1 * phi;
    r -= zoom;

    phi *= freq;
    phi -= turn;

    return vec2(phi, r);
}

void main() {
    vec4 c = vec4(0, 0, 0, 1.0);
    float sigma = 0.5;
    int res = 8;
    float size = sigma * 2;

    float wsum = 0;
    for (int dx = -res; dx <= res; ++dx) {
        for (int dy = -res; dy <= res; ++dy) {
            vec2 d = vec2(dx, dy) / float(res) * size;
            float r = length(d);
            float w = exp(-r*r / (2 * sigma*sigma));
            wsum += w;
        }
    }

    for (int dx = -res; dx <= res; ++dx) {
        for (int dy = -res; dy <= res; ++dy) {
            vec2 d = vec2(dx, dy) / float(res) * size;
            float r = length(d);
            float w = exp(-r*r / (2 * sigma*sigma));
            c += w * texture2D(texture, spiral(v_texcoord + d / width));
        }
    }
    gl_FragColor = 1 - c / wsum;
}
