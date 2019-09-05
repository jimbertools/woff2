

WOFF2.ToTtf = function(woff2input){
    data = new Uint8Array(woff2input);
    var iptr = WOFF2._malloc(data.byteLength);
    WOFF2.HEAPU8.set(data, iptr);

    var converter = new WOFF2.Woff2Converter(iptr, data.byteLength)
    var size = converter.getOutputSize();

    var optr = WOFF2._malloc(size);
    converter.getOutput(optr);

    retVal = new Uint8Array(WOFF2.buffer, optr, size).slice();
    
    WOFF2._free(iptr);
    WOFF2._free(optr);
    return retVal;
}

