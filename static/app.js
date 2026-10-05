const expressionEl = document.getElementById('expression');
const resultEl = document.getElementById('result');
const buttons = document.querySelectorAll('button');
let expression = '';

const updateDisplay = () => {
  expressionEl.textContent = expression || '0';
};

const appendValue = (value) => {
  if (value === '.') {
    const tokens = expression.split(/[-+*/%^]/);
    const lastToken = tokens[tokens.length - 1];
    if (lastToken.includes('.')) return;
  }

  expression += value;
  updateDisplay();
};

const clearAll = () => {
  expression = '';
  resultEl.textContent = '0';
  updateDisplay();
};

const deleteLast = () => {
  expression = expression.slice(0, -1);
  updateDisplay();
};

const computeExpression = async () => {
  if (!expression.trim()) {
    resultEl.textContent = '0';
    return;
  }

  try {
    const response = await fetch('/api/calc', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ expression }),
    });

    const data = await response.json();

    if (data.error) {
      resultEl.textContent = data.error;
      return;
    }

    const formatted = Number(data.result).toString();
    resultEl.textContent = formatted;
    expression = formatted;
    updateDisplay();
  } catch (error) {
    resultEl.textContent = 'Error';
  }
};

buttons.forEach((button) => {
  button.addEventListener('click', async () => {
    const action = button.dataset.action;
    const value = button.dataset.value;

    if (action === 'clear') {
      clearAll();
      return;
    }

    if (action === 'delete') {
      deleteLast();
      return;
    }

    if (action === 'equals') {
      await computeExpression();
      return;
    }

    if (action === 'sqrt') {
      if (!expression.trim()) {
        resultEl.textContent = 'Enter a number first.';
        return;
      }

      expression = `sqrt(${expression})`;
      updateDisplay();
      await computeExpression();
      return;
    }

    if (value !== undefined) {
      appendValue(value);
    }
  });
});

updateDisplay();
