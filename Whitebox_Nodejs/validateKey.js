var _0x1d4c = [
  "lMnYzwf0zuHHCW==",
  "m2qZoti5yMy4za==",
  "CgrHDguOiG==",
  "iIKUzgLNzxn0ka==",
  "Bg9N",
  "iIK7igTLEuHHCW==",
  "AcGIBwq1iIKUDq==",
  "Dg8GpsbYzxf1Aq==",
  "A2v5",
  "iMHLEciPoW==",
  "Aca9ignYExb0BW==",
  "zJy5m2jHztGYna==",
  "CgfYC2u=",
  "y29UC3qGy3j5Ca==",
  "yJDMyMu1mdGYza==",
  "CMuOiMnYExb0BW==",
];
(function (_0x402392, _0x1d4c31) {
  var _0x1415fc = function (_0x2a4f25) {
    while (--_0x2a4f25) {
      _0x402392["push"](_0x402392["shift"]());
    }
  };
  _0x1415fc(++_0x1d4c31);
})(_0x1d4c, 0x171);
var _0x1415 = function (_0x402392, _0x1d4c31) {
  _0x402392 = _0x402392 - 0x0;
  var _0x1415fc = _0x1d4c[_0x402392];
  if (_0x1415["hRcFXf"] === undefined) {
    var _0x2a4f25 = function (_0x31142e) {
      var _0x2e12d0 =
          "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=",
        _0x54b6b9 = String(_0x31142e)["replace"](/=+$/, "");
      var _0x4a7cb8 = "";
      for (
        var _0x4126fb = 0x0, _0xcb88e4, _0x4544bd, _0x4ebfac = 0x0;
        (_0x4544bd = _0x54b6b9["charAt"](_0x4ebfac++));
        ~_0x4544bd &&
        ((_0xcb88e4 =
          _0x4126fb % 0x4 ? _0xcb88e4 * 0x40 + _0x4544bd : _0x4544bd),
        _0x4126fb++ % 0x4)
          ? (_0x4a7cb8 += String["fromCharCode"](
              0xff & (_0xcb88e4 >> ((-0x2 * _0x4126fb) & 0x6))
            ))
          : 0x0
      ) {
        _0x4544bd = _0x2e12d0["indexOf"](_0x4544bd);
      }
      return _0x4a7cb8;
    };
    (_0x1415["Ncsfcg"] = function (_0x3dcea9) {
      var _0x2d8521 = _0x2a4f25(_0x3dcea9);
      var _0x2d077c = [];
      for (
        var _0xb1e023 = 0x0, _0x2b407d = _0x2d8521["length"];
        _0xb1e023 < _0x2b407d;
        _0xb1e023++
      ) {
        _0x2d077c +=
          "%" +
          ("00" + _0x2d8521["charCodeAt"](_0xb1e023)["toString"](0x10))[
            "slice"
          ](-0x2);
      }
      return decodeURIComponent(_0x2d077c);
    }),
      (_0x1415["jhBfJA"] = {}),
      (_0x1415["hRcFXf"] = !![]);
  }
  var _0x3fb401 = _0x1415["jhBfJA"][_0x402392];
  return (
    _0x3fb401 === undefined
      ? ((_0x1415fc = _0x1415["Ncsfcg"](_0x1415fc)),
        (_0x1415["jhBfJA"][_0x402392] = _0x1415fc))
      : (_0x1415fc = _0x3fb401),
    _0x1415fc
  );
};
function validateKey(input) {
  console.log("Reached validateKey")

  try {
    console.log(input)
    json = JSON[_0x1415("0xb")](input);
    console.log('JSON: %j', json)
    var keyHash;
    console.log(
      _0x1415("0xc") +
        _0x1415("0x6") +
        _0x1415("0xe") +
        _0x1415("0x4") +
        _0x1415("0x9") +
        _0x1415("0xf") +
        _0x1415("0x5") +
        _0x1415("0x1") +
        json[_0x1415("0x7")] +
        (_0x1415("0x2") + _0x1415("0x8"))
    );
    eval(
      _0x1415("0xc") +
        _0x1415("0x6") +
        _0x1415("0xe") +
        _0x1415("0x4") +
        _0x1415("0x9") +
        _0x1415("0xf") +
        _0x1415("0x5") +
        _0x1415("0x1") +
        json[_0x1415("0x7")] +
        (_0x1415("0x2") + _0x1415("0x8"))
    );
    if (keyHash == _0x1415("0xd") + _0x1415("0x0") + _0x1415("0xa") + "d2")
      return !![];
  } catch (_0x2fa439) {
    return console[_0x1415("0x3")](_0x2fa439), ![];
  }
  return ![];
}

exports.validateKey = validateKey;
