#include <Python.h>
#include <math.h>

// Apply a simple screen shake effect
static PyObject* apply_screen_shake(PyObject* self, PyObject* args) {
    PyObject* surface;
    int amplitude;
    int frame;
    
    if (!PyArg_ParseTuple(args, "Oii", &surface, &amplitude, &frame)) {
        return NULL;
    }
    
    // Get surface info using pygame's C API
    int width, height;
    if (!PyObject_HasAttrString(surface, "get_size")) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a pygame Surface");
        return NULL;
    }
    
    PyObject* size_tuple = PyObject_CallMethod(surface, "get_size", NULL);
    if (!size_tuple) {
        return NULL;
    }
    
    width = PyLong_AsLong(PyTuple_GetItem(size_tuple, 0));
    height = PyLong_AsLong(PyTuple_GetItem(size_tuple, 1));
    Py_DECREF(size_tuple);
    
    // Create a new surface to hold the result
    PyObject* pygame_module = PyImport_ImportModule("pygame");
    if (!pygame_module) {
        return NULL;
    }
    
    PyObject* new_surface = PyObject_CallMethod(pygame_module, "Surface", "(ii)", width, height);
    Py_DECREF(pygame_module);
    
    if (!new_surface) {
        return NULL;
    }
    
    // Calculate shake offset
    int offset_x = (int)(sin(frame * 0.5) * amplitude);
    int offset_y = (int)(cos(frame * 0.7) * amplitude);
    
    // Apply the shake by blitting the source surface with an offset
    PyObject* result = PyObject_CallMethod(new_surface, "blit", "O(ii)", surface, offset_x, offset_y);
    if (!result) {
        Py_DECREF(new_surface);
        return NULL;
    }
    Py_DECREF(result);
    
    return new_surface;
}

// Apply a simple wave distortion effect
static PyObject* apply_wave_effect(PyObject* self, PyObject* args) {
    PyObject* surface;
    float time;
    float amplitude;
    float frequency;
    
    if (!PyArg_ParseTuple(args, "Offf", &surface, &time, &amplitude, &frequency)) {
        return NULL;
    }
    
    // Get surface dimensions
    PyObject* size_tuple = PyObject_CallMethod(surface, "get_size", NULL);
    if (!size_tuple) {
        return NULL;
    }
    
    int width = PyLong_AsLong(PyTuple_GetItem(size_tuple, 0));
    int height = PyLong_AsLong(PyTuple_GetItem(size_tuple, 1));
    Py_DECREF(size_tuple);
    
    // Create new surface for the result
    PyObject* pygame_module = PyImport_ImportModule("pygame");
    if (!pygame_module) {
        return NULL;
    }
    
    PyObject* surfarray_module = PyImport_ImportModule("pygame.surfarray");
    if (!surfarray_module) {
        Py_DECREF(pygame_module);
        return NULL;
    }
    
    PyObject* new_surface = PyObject_CallMethod(pygame_module, "Surface", "(ii)", width, height);
    Py_DECREF(pygame_module);
    
    if (!new_surface) {
        Py_DECREF(surfarray_module);
        return NULL;
    }
    
    // Get array representation of surfaces
    PyObject* src_array = PyObject_CallMethod(surfarray_module, "array3d", "O", surface);
    PyObject* dst_array = PyObject_CallMethod(surfarray_module, "array3d", "O", new_surface);
    Py_DECREF(surfarray_module);
    
    if (!src_array || !dst_array) {
        Py_XDECREF(src_array);
        Py_XDECREF(dst_array);
        Py_DECREF(new_surface);
        return NULL;
    }
    
    // This is simplified - in a real implementation we would 
    // directly manipulate the array data using the C API
    // but for this example, we'll just return the original surface
    
    // Clean up
    Py_DECREF(src_array);
    Py_DECREF(dst_array);
    
    // For now just return the original surface (placeholder)
    Py_INCREF(surface);
    Py_DECREF(new_surface);
    return surface;
}

// Module method table
static PyMethodDef ShaderMethods[] = {
    {"screen_shake", apply_screen_shake, METH_VARARGS, "Apply screen shake effect"},
    {"wave_effect", apply_wave_effect, METH_VARARGS, "Apply wave distortion effect"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef shadermodule = {
    PyModuleDef_HEAD_INIT,
    "shaders",         // name of module
    "C shader effects for pygame",  // module documentation
    -1,                // size of per-interpreter state or -1
    ShaderMethods      // method table
};

// Module initialization function
PyMODINIT_FUNC PyInit_shaders(void) {
    return PyModule_Create(&shadermodule);
}
