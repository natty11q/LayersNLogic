
from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *
# from ApplicationEngine.src.Graphics.Renderer.Renderer import *


from OpenGL.GL import * #type: ignore
from PIL import Image


class Texture():
    def __init__(self, image_path, transparent : bool = False):
        
        if os.path.exists(image_path):
            image = Image.open(image_path)
        else:
            image = Image.open("ApplicationEngine/Assets/DefaultTextires/Debugempty.png")

        tex_np = np.array(image, dtype=np.uint8)
        if image.mode == "RGB":
            tex_np = np.array(image.convert("RGB"), dtype=np.uint8)
        if image.mode == "RGBA":
            tex_np = np.array(image.convert("RGBA"), dtype=np.uint8)
        tex_np = np.flipud(tex_np)
        self.tex_height, self.tex_width, _ = tex_np.shape

        self.texture_id = glGenTextures(1)
        
        self.hasTransparent = transparent
        
        glBindTexture(GL_TEXTURE_2D, self.texture_id)


        if image.mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.tex_width, self.tex_height,
                     0 , GL_RGB, GL_UNSIGNED_BYTE, tex_np)
        if image.mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.tex_width, self.tex_height,
                     0 , GL_RGBA, GL_UNSIGNED_BYTE, tex_np)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)  # Generate mipmaps for scaling
        glBindTexture(GL_TEXTURE_2D, 0)  # Unbind the texture

    def Bind(self):
        from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer
        # if not glIsTexture(self.texture_id):
        #     print("Error: One or both textures are not valid.")
        Renderer.BindTexture(self.texture_id)
        
    def UnBind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    # def __del__(self):
    #     glDeleteTextures(1, [self.texture_id])