// Copyright (C) 2013 Alexandre Rames <alexandre@uop.re>
// rejit is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include <iostream>

#include "globals.h"

namespace rejit {
namespace internal {

// Indentation helpers ---------------------------------------------------------
const char* kIndentString = "  ";
int kIndentLevel = 0;


uint64_t FirstBytesMask(int n) {
  if (n >= kPointerSize) return kMaxUInt64;
  uint64_t mask = (1ULL << (n * kBitsPerByte)) - 1ULL;
  return mask;
}

} }  // namespace rejit::internal

