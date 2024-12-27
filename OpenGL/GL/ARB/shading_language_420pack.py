'''OpenGL extension ARB.shading_language_420pack

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.shading_language_420pack to provide a more 
Python-friendly API

Overview (from the spec)
	
	This is a language feature only extension formed from changes made
	to version 4.20 of GLSL.  It includes:
	
	* Add line-continuation using '\', as in C++.
	
	* Change from ASCII to UTF-8 for the language character set and also 
	  allow any characters inside comments.
	
	* Allow implicit conversions of return values to the declared type of 
	  the function.
	
	* The *const* keyword can be used to declare variables within a function 
	  body with initializer expressions that are not constant expressions.
	
	* Qualifiers on variable declarations no longer have to follow a strict 
	  order. The layout qualifier can be used multiple times, and multiple 
	  parameter qualifiers can be used.  However, this is not as
	  straightforward as saying declarations have arbitrary lists of 
	  initializers.  Typically, one qualifier from each class of qualifiers
	  is allowed, so care is now taken to classify them and say so.  Then, 
	  of these, order restrictions are removed.
	
	* Add layout qualifier identifier "binding" to bind the location of a
	  uniform block.  This requires version 1.4 of GLSL.  If this extension
	  is used with an earlier version than 1.4, this feature is not present.
	
	* Add layout qualifier identifier "binding" to bind units to sampler 
	  and image variable declarations.
	
	* Add C-style curly brace initializer lists syntax for initializers. 
	  Full initialization of aggregates is required when these are used.
	
	* Allow ".length()" to be applied to vectors and matrices, returning 
	  the number of components or columns.
	
	* Allow swizzle operations on scalars.
	
	* Built-in constants for gl_MinProgramTexelOffset and 
	  gl_MaxProgramTexelOffset.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/shading_language_420pack.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.shading_language_420pack import *
from OpenGL.raw.GL.ARB.shading_language_420pack import _EXTENSION_NAME

def glInitShadingLanguage420PackARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION