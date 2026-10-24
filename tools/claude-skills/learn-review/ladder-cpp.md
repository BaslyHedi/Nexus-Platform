# C++ ladder

The concepts of the learning review, in the order they are introduced. Shared by every Nexus repository written in C++. The FBL uses C++17, freestanding subset (SW-03): no heap, no exceptions, no RTTI. A concept is `new`, `seen` (a review explained it) or `mastered` (Hedi used it right without help). The review takes the first `new` concept that fits the code that was written.

## 1. Basics: C++ where C differs

| Concept | Status |
|---|---|
| Classes: `public` and `private`, member functions, the trailing `_` of members | seen |
| Namespaces and `::` | mastered |
| Getters, `const` member functions | mastered |
| Integral promotion: `uint8_t` and `uint16_t` become `int` in arithmetic | seen |
| `static_cast` instead of the C cast | mastered |
| `noexcept` and why the freestanding build wants it | seen |
| Declarations only at namespace scope: no statements outside a function | seen |
| `inline` and the one-definition rule: `constexpr` functions and bodies in the class are implicitly inline | seen |
| Declaration and definition must agree: `constexpr`, `noexcept`, `const` | seen |
| Temporaries and object lifetime: `T()` is a new object each time | seen |
| Constructors: member initializer list, default member initializers | mastered |
| `const` (not changed after it is set) versus `constexpr` (known at compile time) | seen |
| Header-only versus `.hpp` and `.cpp`: what each costs and hides | seen |
| References versus pointers, `const&` parameters | seen |
| `static constexpr` data members | new |
| Overloading (same name, different parameters) versus overriding (`virtual`), overload resolution | seen |

## 2. Types that carry meaning

| Concept | Status |
|---|---|
| `std::extent_v`, `std::size` and letting the compiler count | mastered |
| `static_assert` as a compile-time test | mastered |
| `constexpr` lambdas, called immediately (C++17) | seen |
| `enum class` and its underlying type | new |
| `std::array` instead of a C array | new |
| `explicit` constructors | new |
| `= default`, `= delete`, the rule of zero | new |
| A view type: pointer and size held together, in place of C++20 `std::span` | new |

## 3. Generic code

| Concept | Status |
|---|---|
| Function templates | new |
| Class templates and non-type template parameters | new |
| A table computed at compile time (the CRC table as a `constexpr` array) | new |
| `if constexpr` | new |
| `<type_traits>` in templates, `std::enable_if` | new |

## 4. Firmware C++

| Concept | Status |
|---|---|
| Registers: `volatile`, strong types for addresses and bit fields | new |
| RAII for hardware: a guard that disables and restores interrupts | new |
| Move semantics, and why the FBL rarely needs them | new |
| Placement `new` and alignment | new |
| What costs code size: virtual functions, templates, inlining | new |
