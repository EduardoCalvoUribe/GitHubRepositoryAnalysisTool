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
