// Copyright (C) 2013 Alexandre Rames <alexandre@coreperf.com>
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

#ifndef REJIT_ASSEMBLER_H_
#define REJIT_ASSEMBLER_H_

#include "globals.h"

namespace rejit {
namespace internal {


#ifdef REJIT_TARGET_ARCH_X64
#include "x64/assembler-x64.h"
#include "x64/assembler-x64-inl.h"
#else
#error Unkown target architecture.
#endif

} }  // namespace rejit::internal

#endif  // REJIT_ASSEMBLER_H_
