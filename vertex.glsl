uniform float aspect = 1.0;
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;

void main() {
    vec2 p = position;
    p.y *= aspect;
    gl_Position = vec4(p, 0.0, 1.0);
    v_texcoord = texcoord;
}
