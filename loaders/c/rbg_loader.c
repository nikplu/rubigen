#include "rbg_loader.h"

#if defined(__linux__) || defined(__unix__) || defined(_POSIX_VERSION)
#include <dlfcn.h>

rbg_library *rbg_open_library(const char *name)
{
	return (rbg_library *)dlopen(name, RTLD_LAZY);
}

void rbg_close_library(rbg_library *lib)
{
	dlclose((void*)lib);
}

void *rbg_get_sym(void *user_arg, const char *name)
{
	return dlsym((void*)user_arg, name);
}
#elif defined(_WIN32)
#define VC_EXTRALEAN
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

rbg_library *rbg_open_library(const char *name)
{
	return (rbg_library *)LoadLibraryA(name);
}

void rbg_close_library(rbg_library *lib)
{
	FreeLibrary((HMODULE)lib);
}

void *rbg_get_sym(void *user_arg, const char *name)
{
	return GetProcAddress((HMODULE)user_arg, name);
}
#endif
