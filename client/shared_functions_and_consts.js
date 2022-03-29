export const MAX_SIZE_OF_IMAGE = 500; // square - will be true for both width and height

export function resizeImage(originalWidth, originalHeight) {
    let i = 1;
    let width = originalWidth;
    let height = originalHeight;
    while (width > MAX_SIZE_OF_IMAGE || height > MAX_SIZE_OF_IMAGE) {
        width = originalWidth / i;
        height = originalHeight / i;
        i = i + 0.5;
    }
    return [width, height];
}