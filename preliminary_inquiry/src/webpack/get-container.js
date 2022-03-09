/**
 * Get a div (append into page container) to
 * append a viz
 * @returns {HTMLDivElement}
 */

export default function (container) {
    const div = document.createElement('div');
    div.classList.add('block', 'viz')
    container.appendChild(div)
    return div;
}