'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_VERSION_GL_2_1'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_VERSION_GL_2_1',error_checker=_errors._error_checker)
GL_COMPRESSED_SLUMINANCE=_C('GL_COMPRESSED_SLUMINANCE',0x8C4A)
GL_COMPRESSED_SLUMINANCE_ALPHA=_C('GL_COMPRESSED_SLUMINANCE_ALPHA',0x8C4B)
GL_COMPRESSED_SRGB=_C('GL_COMPRESSED_SRGB',0x8C48)
GL_COMPRESSED_SRGB_ALPHA=_C('GL_COMPRESSED_SRGB_ALPHA',0x8C49)
GL_CURRENT_RASTER_SECONDARY_COLOR=_C('GL_CURRENT_RASTER_SECONDARY_COLOR',0x845F)
GL_FLOAT_MAT2x3=_C('GL_FLOAT_MAT2x3',0x8B65)
GL_FLOAT_MAT2x4=_C('GL_FLOAT_MAT2x4',0x8B66)
GL_FLOAT_MAT3x2=_C('GL_FLOAT_MAT3x2',0x8B67)
GL_FLOAT_MAT3x4=_C('GL_FLOAT_MAT3x4',0x8B68)
GL_FLOAT_MAT4x2=_C('GL_FLOAT_MAT4x2',0x8B69)
GL_FLOAT_MAT4x3=_C('GL_FLOAT_MAT4x3',0x8B6A)
GL_PIXEL_PACK_BUFFER=_C('GL_PIXEL_PACK_BUFFER',0x88EB)
GL_PIXEL_PACK_BUFFER_BINDING=_C('GL_PIXEL_PACK_BUFFER_BINDING',0x88ED)
GL_PIXEL_UNPACK_BUFFER=_C('GL_PIXEL_UNPACK_BUFFER',0x88EC)
GL_PIXEL_UNPACK_BUFFER_BINDING=_C('GL_PIXEL_UNPACK_BUFFER_BINDING',0x88EF)
GL_SLUMINANCE=_C('GL_SLUMINANCE',0x8C46)
GL_SLUMINANCE8=_C('GL_SLUMINANCE8',0x8C47)
GL_SLUMINANCE8_ALPHA8=_C('GL_SLUMINANCE8_ALPHA8',0x8C45)
GL_SLUMINANCE_ALPHA=_C('GL_SLUMINANCE_ALPHA',0x8C44)
GL_SRGB=_C('GL_SRGB',0x8C40)
GL_SRGB8=_C('GL_SRGB8',0x8C41)
GL_SRGB8_ALPHA8=_C('GL_SRGB8_ALPHA8',0x8C43)
GL_SRGB_ALPHA=_C('GL_SRGB_ALPHA',0x8C42)
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix2x3fv(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix2x4fv(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix3x2fv(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix3x4fv(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix4x2fv(location,count,transpose,value):pass
@_f
@_p.types(None,_cs.GLint,_cs.GLsizei,_cs.GLboolean,arrays.GLfloatArray)
def glUniformMatrix4x3fv(location,count,transpose,value):pass
