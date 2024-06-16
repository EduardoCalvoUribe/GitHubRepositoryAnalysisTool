export const generateColorBuckets = (colorBuckets) => {
    const colors = [];
    for (let i = 0; i < colorBuckets; i++) {
      const r = Math.round(255 - (255 * i / (colorBuckets - 1)));
      const g = Math.round(255 * i / (colorBuckets - 1));
      const b = 0;
      colors.push(`rgb(${r}, ${g}, ${b})`);
    }
    return colors;
  };
  
  export const getGradientColor = (score, colorBuckets) => {
    const colors = generateColorBuckets(colorBuckets);
    const index = Math.min(Math.floor(score / 10), colors.length - 1);
    return colors[index];
  };
  