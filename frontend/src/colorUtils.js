// Copyright 2024 Radboud University, Modern Software Development Techniques

// Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

// 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

// 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

// 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

/**
 * Generates an array of gradient colors from red to green.
 *
 * @param {number} colorBuckets - The number of color buckets to generate.
 * @returns {string[]} An array of RGB color strings representing the gradient.
 */
export const generateColorBuckets = (colorBuckets) => {
  const colors = [];
  // Loop through the color buckets and calculate rgb values.
  for (let i = 0; i < colorBuckets; i++) {
    const r = Math.round(255 - (255 * i / (colorBuckets - 1)));
    const g = Math.round(255 * i / (colorBuckets - 1));
    const b = 0;
    colors.push(`rgb(${r}, ${g}, ${b})`);
  }
  return colors;
};

/**
 * Gets the gradient color corresponding to a given score.
 *
 * @param {number} score - The score to determine the color for.
 * @param {number} colorBuckets - The number of color buckets to use.
 * @returns {string} The RGB color string corresponding to the score.
 */
export const getGradientColor = (score, colorBuckets) => {
  const colors = generateColorBuckets(colorBuckets);
  const index = Math.min(Math.floor(score / 10), colors.length - 1);
  return colors[index];
};
