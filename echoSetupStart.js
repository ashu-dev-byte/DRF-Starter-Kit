// ANSI escape codes
const boldBlue = '\x1b[1;34m';
const blue = '\x1b[34m';
const end = '\x1b[0m';

/**
 * Formats a message with the specified color and style.
 * @param {string} text - The text to format.
 * @param {string} style - The ANSI escape code for the style.
 * @returns {string} - The formatted message.
 */
const formatMessage = (text, style) => `${style}${text}${end}`;

const msg1 = formatMessage('Starting project setup:', boldBlue);
const msg2 = `${formatMessage('Installing dependencies...', blue)}\n`;

console.log(msg1);
console.log(msg2);
