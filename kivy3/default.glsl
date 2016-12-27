---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

// inside VS, read-only
attribute vec3 v_pos;
attribute vec3 v_normal;
attribute vec4 v_color;
attribute vec2 v_tc0;

// from python, read-only
uniform mat4 modelview_mat;
uniform mat4 projection_mat;
uniform mat4 normal_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

// used later in FS
varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec4 frag_color;
varying vec2 uv_vec;


void main (void) {
    // fetch read-only for later use
    normal_vec = vec4(v_normal, 0.0);
    frag_color = v_color;
    uv_vec = v_tc0;

    vec4 pos = modelview_mat * vec4(v_pos, 1.0);
    vertex_pos = pos;

    // required shader clip-space output
    gl_Position = projection_mat * pos;
}


---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

// from VS
varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec4 frag_color;
varying vec2 uv_vec;

// from python, read-only
uniform mat4 modelview_mat;
uniform mat4 projection_mat;
uniform mat4 normal_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

uniform vec3 camera_pos;
uniform vec3 Ka; // color (ambient)
uniform vec3 Kd; // diffuse color
uniform vec3 Ks; // specular color
uniform float Tr; // transparency
uniform float Ns; // shininess
uniform float tex_ratio;

uniform vec3 light_pos;
uniform float light_intensity;

uniform sampler2D tex; // texture


void main (void){
    // pull colors from texture
    vec4 tex_color = texture2D(tex, uv_vec);

    // force lightPos to lower-left (like in Kivy)
    vec4 lightPos = model_mat * vec4(light_pos, 0.0) - gl_FragCoord;
    float lightPosLen = length(lightPos);

    vec4 v_normal = normalize(normal_mat * normal_vec);
    vec4 vertex_world = modelview_mat * vertex_pos;
    vec4 v_light = vec4(light_pos, 1.0) - vertex_world;

    // set ambient, diffuse, specular color
    vec3 Ia = Ka * light_intensity / lightPosLen;
    vec3 Id = Kd * max(dot(v_light, v_normal), 0.0);
    vec3 Is = Ks * pow(max(dot(v_light, v_normal), 0.0), Ns);

    // modify texture color by light intensity
    tex_color = vec4(
        tex_color.rgb * light_intensity / lightPosLen,
        tex_color[3]
    );

    // required shader output
    // window-space fragment color with texture
    gl_FragColor = vec4(Ia + Id + Is, Tr);
    gl_FragColor = mix(gl_FragColor, tex_color, tex_ratio);
}
