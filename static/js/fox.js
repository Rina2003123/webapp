// fox.js
class Fox {
  constructor(containerId = 'fox-container') {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = containerId;
      document.body.appendChild(this.container);
    }
    this.setNeutral();
  }

  setEmotion(emotion) {
    const imagePath = `{{ url_for('static', filename='images/fox/${emotion}.png') }}`;
    this.container.innerHTML = `
      <img src="${imagePath}" 
           alt="Fox ${emotion}" 
           style="width: 100%; height: 100%; object-fit: contain;">`;
  }

  setNeutral() { this.setEmotion('neutral'); }
  setHappy() { this.setEmotion('happy'); }
  setSad() { this.setEmotion('sad'); }
}

// Делаем класс доступным глобально
window.Fox = Fox;