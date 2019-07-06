#pragma once

typedef struct rbg_library_t rbg_library;
rbg_library *rbg_open_library(const char *name);
void rbg_close_library(rbg_library *lib);
void *rbg_get_sym(void *user_arg, const char *name);

#ifdef __cplusplus
#include <memory>

namespace rbg {

namespace detail {

struct LibraryDeleter
{
	void operator()(::rbg_library *ptr)
	{
		::rbg_close_library(ptr);
	}
};

} // namespace detail

using RbgLibraryPtr = std::unique_ptr<::rbg_library, detail::LibraryDeleter>;

inline RbgLibraryPtr open_library(const char *name)
{
	return RbgLibraryPtr(::rbg_open_library(name));
}

} // namespace rbg

#endif
