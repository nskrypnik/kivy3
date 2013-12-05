---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3  v_pos;
attribute vec4  v_color;
attribute vec2  v_tc0;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;

varying vec4 frag_color;
varying vec2 uv_vec;

void main (void) {
    vec4 pos = modelview_mat * vec4(v_pos,1.0);
    gl_Position = projection_mat * pos;
    frag_color = v_color;
    uv_vec = v_tc0;
}


---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 frag_color;
varying vec2 uv_vec;

uniform sampler2D tex;

void main (void){
    vec4 color = texture2D(tex, uv_vec);
    gl_FragColor = color;
}