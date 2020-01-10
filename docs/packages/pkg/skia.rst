.. spelling::

    skia

.. index::
  single: graphics ; skia

.. _pkg.skia:

skia
====

-  `Official <https://skia.org>`__
-  `Hunterized <https://github.com/cpp-pm/skia>`__
-  `Example <https://github.com/cpp-pm/hunter/blob/master/examples/skia/CMakeLists.txt>`__
-  Added by `Rahul Sheth <https://github.com/rbsheth>`__ (`pr-N <https://github.com/cpp-pm/hunter/pull/N>`__)

Valid CMake arguments:
- `SKIA_BUILD_MODULE_SKSHAPER` - build the SkShaper module (Default `ON`)
- `SKIA_ENABLE_ATLAS_TEXT` - build the AtlasText module (Default `ON`)
- `SKIA_ENABLE_OPENCL` - build with OpenCL support (Default `OFF`)
- `SKIA_ENABLE_VULKAN` - build with Vulkan support (Default `OFF`)
- `SKIA_STATIC` - build static libraries (Default `ON`)
- `SKIA_SHARED` - build shared libraries, overrides `SKIA_STATIC` (Default `OFF`)

You have to explicitly switch to these versions of dependencies:

.. literalinclude:: /../examples/Urho3D/config.cmake
  :language: cmake
  :start-after: # DOCUMENTATION_START {
  :end-before: # DOCUMENTATION_END }

This is because Skia requires `libjpeg-turbo`, which conflicts with the regular `Jpeg` library. A `chromium-` version of `ZLIB` is recommended but not required.

.. literalinclude:: /../examples/skia/CMakeLists.txt
  :language: cmake
  :start-after: # DOCUMENTATION_START {
  :end-before: # DOCUMENTATION_END }
