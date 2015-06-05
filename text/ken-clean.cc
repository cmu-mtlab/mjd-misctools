#include <unicode/uchar.h>
#include <unicode/uscript.h>

#include <iostream>
#include <fstream>
#include <numeric>
#include <string.h>
#include <stdlib.h>

bool Include(const std::string &line) {
  int32_t offset = 0;
  int32_t length = static_cast<int32_t>(line.size());
  size_t counts[USCRIPT_CODE_LIMIT];
  memset(counts, 0, sizeof(counts));
  size_t angle = 0;
  while (offset < length) {
    UChar32 character;
    U8_NEXT(line.data(), offset, length, character);
    // Avoid bad unicode and control characters
    if (character < 32) return false;
    UErrorCode err = U_ZERO_ERROR;
    UScriptCode script = uscript_getScript(character, &err);
    if (U_FAILURE(err) || script == USCRIPT_INVALID_CODE) return false;
    ++counts[script];
    if (character == '<' || character == '>') ++angle;
    // Do not allow unicode newlines
    if (character == 133 || character == 8232 || character == 8233) return false;
  }
  // Check for reasonable concentration of Latin characters
  float total = static_cast<float>(std::accumulate(counts, counts + USCRIPT_CODE_LIMIT, 0));
  if (static_cast<float>(counts[USCRIPT_LATIN] + counts[USCRIPT_INHERITED] + counts[USCRIPT_COMMON] - angle) < total * 0.9) return false;
  if (static_cast<float>(counts[USCRIPT_LATIN]) < total * 0.5) return false;
  return true;
}

int main(int argc, char **argv) {
  if (argc != 5) {
    std::cerr << "usage: " << argv[0] << " in.fr in.en out.fr out.en\n";
    exit(1);
  }

  std::ifstream in_fr;
  std::ifstream in_en;
  std::ofstream out_fr;
  std::ofstream out_en;
  in_fr.open(argv[1]);
  in_en.open(argv[2]);
  out_fr.open(argv[3]);
  out_en.open(argv[4]);

  std::string line_fr;
  std::string line_en;
  while (getline(in_fr, line_fr)) {
    getline(in_en, line_en);
    if (Include(line_fr) && Include(line_en)) {
      out_fr << line_fr << '\n';
      out_en << line_en << '\n';
    }
  }

  in_fr.close();
  in_en.close();
  out_fr.close();
  out_en.close();
}
