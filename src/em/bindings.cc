#include <iostream>

#include <emscripten.h>
#include <emscripten/bind.h>
#include <woff2/decode.h>

using emscripten::allow_raw_pointers;
using emscripten::class_;
using emscripten::optional_override;
class Woff2Converter
{
    uint8_t *input;
    size_t size;

public:
    Woff2Converter(uint8_t *input, size_t size) : input(input), size(size){};

    uint32_t getOutputSize()
    {
        return std::min(woff2::ComputeWOFF2FinalSize(input, size), woff2::kDefaultMaxSize);
    }
    void getOutput(uint8_t *output, size_t outputLength)
    {
        woff2::ConvertWOFF2ToTTF(output, outputLength, input, size);
    }
};

EMSCRIPTEN_BINDINGS(WOFF2)
{
    class_<Woff2Converter>("Woff2Converter")

        .class_function("make", optional_override([](uintptr_t /* uint8_t*  */ ptr, size_t size) -> Woff2Converter {
                            uint8_t *bytes = reinterpret_cast<uint8_t *>(ptr);

                            return Woff2Converter(bytes, size);
                        }),
                        allow_raw_pointers())
        .function("getOutputSize", &Woff2Converter::getOutputSize, allow_raw_pointers())
        .function("getOutput", optional_override([](Woff2Converter &self, uintptr_t /* uint8_t*  */ ptr, size_t size) -> void {
                      uint8_t *bytes = reinterpret_cast<uint8_t *>(ptr);
                      self.getOutput(bytes, size);
                  }),
                  allow_raw_pointers());
}