document.addEventListener('DOMContentLoaded', function() {
  // Initialize data structures
  const expenses = [];
  const budgets = {
    groceries: 0,
    utilities: 0,
    rent: 0,
    entertainment: 0,
    transportation: 0,
    dining: 0,
    healthcare: 0,
    other: 0
  };
  
  // Thresholds for warning and danger zones
  const WARNING_THRESHOLD = 0.75; // 75% of budget - Orange
  const DANGER_THRESHOLD = 1.0; // 100% of budget - Red
  
  // Elements
  const expenseList = document.getElementById('expense-list');
  const budgetBars = document.getElementById('budget-bars');
  const addExpenseBtn = document.getElementById('add-expense-btn');
  const editBudgetBtn = document.getElementById('edit-budget-btn');
  const setBudgetBtn = document.getElementById('set-budget-btn');
  const budgetForm = document.getElementById('budget-form');
  
  // Stats elements
  const totalSpentEl = document.getElementById('total-spent');
  const totalBudgetEl = document.getElementById('total-budget');
  const remainingBudgetEl = document.getElementById('remaining-budget');
  
  // Color map for categories
  const categoryColors = {
    groceries: '#3b82f6',
    utilities: '#10b981',
    rent: '#6366f1',
    entertainment: '#f59e0b',
    transportation: '#8b5cf6',
    dining: '#ef4444',
    healthcare: '#06b6d4',
    other: '#6b7280'
  };
  
  // Format currency
  function formatCurrency(amount) {
    return '₹' + amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  }
  
  // Update the summary stats
  function updateSummaryStats() {
    // Calculate total spent
    const totalSpent = expenses.reduce((total, expense) => total + expense.amount, 0);
    // Calculate total budget
    const totalBudget = Object.values(budgets).reduce((total, budget) => total + budget, 0);
    // Calculate remaining budget
    const remainingBudget = totalBudget - totalSpent;
    
    // Update the UI
    totalSpentEl.textContent = formatCurrency(totalSpent);
    totalBudgetEl.textContent = formatCurrency(totalBudget);
    remainingBudgetEl.textContent = formatCurrency(remainingBudget);
    
    // Apply color to remaining budget based on status
    if (remainingBudget < 0) {
      remainingBudgetEl.style.color = '#ef4444'; // Red for overspent
    } else if (remainingBudget < totalBudget * 0.2) {
      remainingBudgetEl.style.color = '#f59e0b'; // Yellow for warning
    } else {
      remainingBudgetEl.style.color = '#10b981'; // Green for good
    }
  }
  
  // Render the expense list
  function renderExpenseList() {
    // Clear the existing list
    expenseList.innerHTML = '';
    
    // If no expenses, show a message
    if (expenses.length === 0) {
      expenseList.innerHTML = `
        <div class="expense-item">
          <div class="expense-details">
            <span>Add your first expense</span>
            <span class="expense-category">Get started</span>
          </div>
        </div>
      `;
      return;
    }
    
    // Sort expenses by most recent first
    const sortedExpenses = [...expenses].reverse();
    
    // Create expense items
    sortedExpenses.forEach((expense, index) => {
      const expenseItem = document.createElement('div');
      expenseItem.className = 'expense-item';
      expenseItem.innerHTML = `
        <div class="expense-details">
          <span>${expense.description}</span>
          <span class="expense-category">${expense.category.charAt(0).toUpperCase() + expense.category.slice(1)}</span>
        </div>
        <div>
          <span class="expense-amount">${formatCurrency(expense.amount)}</span>
          <div class="expense-actions">
            <button class="btn-icon" data-index="${index}">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
              </svg>
            </button>
          </div>
        </div>
      `;
      expenseList.appendChild(expenseItem);
      
      // Add delete event listener
      const deleteBtn = expenseItem.querySelector('.btn-icon');
      deleteBtn.addEventListener('click', () => {
        const expenseIndex = expenses.length - 1 - index;
        expenses.splice(expenseIndex, 1);
        renderExpenseList();
        renderBudgetBars();
        updateSummaryStats();
        saveData();
      });
    });
  }
  
  function renderBudgetBars() {
    // Clear the existing bars
    budgetBars.innerHTML = '';
    
    // Check if any budgets are set
    const hasBudgets = Object.values(budgets).some(budget => budget > 0);
    if (!hasBudgets) {
      budgetBars.innerHTML = `
        <div class="budget-category">
          <div class="budget-header">
            <span class="budget-label">Set your first budget</span>
            <span class="budget-values">Click "Edit Budget" to get started</span>
          </div>
        </div>
      `;
      return;
    }
    
    // Calculate spent by category
    const spentByCategory = {};
    Object.keys(budgets).forEach(category => {
      spentByCategory[category] = expenses
        .filter(expense => expense.category === category)
        .reduce((total, expense) => total + expense.amount, 0);
    });
    
    // Create budget bars for categories with budgets
    Object.keys(budgets).filter(category => budgets[category] > 0).forEach(category => {
      const spent = spentByCategory[category] || 0;
      const budget = budgets[category];
      const spentRatio = spent / budget;
      
      const budgetCategory = document.createElement('div');
      budgetCategory.className = 'budget-category';
      budgetCategory.setAttribute('data-category', category);
      
      // Create the header with labels and delete button
      const headerHTML = `
        <div class="budget-header">
          <span class="budget-label">
            ${category.charAt(0).toUpperCase() + category.slice(1)}
            <button class="delete-budget-btn" data-category="${category}">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
              </svg>
            </button>
          </span>
          <span class="budget-values">${formatCurrency(spent)} / ${formatCurrency(budget)}</span>
        </div>
      `;
      
      // Create the progress bar container
      const progressBarContainer = document.createElement('div');
      progressBarContainer.className = 'progress-bar';
      
      // Create the segmented progress container
      const segmentedProgress = document.createElement('div');
      segmentedProgress.className = 'segmented-progress';
      
      // Base color for normal spending
      const baseColor = categoryColors[category];
      const warningColor = '#f59e0b'; // Orange for warning
      const dangerColor = '#ef4444'; // Red for over budget
      
      // Calculate segment widths
      let normalSegmentWidth = 0;
      let warningSegmentWidth = 0;
      let dangerSegmentWidth = 0;
      
      if (spentRatio <= WARNING_THRESHOLD) {
        normalSegmentWidth = spentRatio * 100;
      } else if (spentRatio <= DANGER_THRESHOLD) {
        normalSegmentWidth = WARNING_THRESHOLD * 100;
        warningSegmentWidth = (spentRatio - WARNING_THRESHOLD) * 100;
      } else {
        normalSegmentWidth = WARNING_THRESHOLD * 100;
        warningSegmentWidth = (DANGER_THRESHOLD - WARNING_THRESHOLD) * 100;
        dangerSegmentWidth = (spentRatio - DANGER_THRESHOLD) * 100;
      }
      
      // Add segments to bar
      if (normalSegmentWidth > 0) {
        const normalSegment = document.createElement('div');
        normalSegment.className = 'progress-segment';
        normalSegment.style.width = `${normalSegmentWidth}%`;
        normalSegment.style.backgroundColor = baseColor;
        segmentedProgress.appendChild(normalSegment);
      }
      
      if (warningSegmentWidth > 0) {
        const warningSegment = document.createElement('div');
        warningSegment.className = 'progress-segment';
        warningSegment.style.width = `${warningSegmentWidth}%`;
        warningSegment.style.backgroundColor = warningColor;
        segmentedProgress.appendChild(warningSegment);
      }
      
      if (dangerSegmentWidth > 0) {
        const dangerSegment = document.createElement('div');
        dangerSegment.className = 'progress-segment';
        dangerSegment.style.width = `${dangerSegmentWidth}%`;
        dangerSegment.style.backgroundColor = dangerColor;
        segmentedProgress.appendChild(dangerSegment);
      }
      
      // Append segments to container
      progressBarContainer.appendChild(segmentedProgress);
      
      budgetCategory.innerHTML = headerHTML;
      budgetCategory.appendChild(progressBarContainer);
      
      // Threshold markers
      const thresholdContainer = document.createElement('div');
      thresholdContainer.className = 'threshold-markers';
      thresholdContainer.style.position = 'relative';
      thresholdContainer.style.marginTop = '4px';
      thresholdContainer.style.height = '20px';
      thresholdContainer.style.width = '100%';
      
      // Adjusted for dynamic scale (spent or budget, whichever is greater)
      const scaleBase = Math.max(spent, budget);
      const warningValue = budget * WARNING_THRESHOLD;
      const dangerValue = budget;
      const warningPosition = (warningValue / scaleBase) * 100;
      const dangerPosition = (dangerValue / scaleBase) * 100;
      const spentPosition = (spent / scaleBase) * 100;
      
      let thresholdHTML = '';
      
      // Start marker ₹0
      thresholdHTML += `
        <span style="position: absolute; left: 0%; top: 0; font-size: 0.75rem; color: ${baseColor};">₹0</span>
        <div style="position: absolute; left: 0%; top: -4px; height: 4px; width: 1px; background-color: ${baseColor};"></div>
      `;
      
      // Warning marker
      thresholdHTML += `
        <span style="position: absolute; left: ${warningPosition}%; transform: translateX(-50%); top: 0; font-size: 0.75rem; color: ${warningColor};">₹${Math.round(warningValue)}</span>
        <div style="position: absolute; left: ${warningPosition}%; transform: translateX(-50%); top: -4px; height: 4px; width: 1px; background-color: ${warningColor};"></div>
      `;
      
      // Danger marker
      thresholdHTML += `
        <span style="position: absolute; left: ${dangerPosition}%; transform: translateX(-50%); top: 0; font-size: 0.75rem; color: ${dangerColor};">₹${Math.round(dangerValue)}</span>
        <div style="position: absolute; left: ${dangerPosition}%; transform: translateX(-50%); top: -4px; height: 4px; width: 1px; background-color: ${dangerColor};"></div>
      `;
      
      // Spent marker if overspent
      if (spent > dangerValue) {
        thresholdHTML += `
          <span style="position: absolute; left: ${spentPosition}%; transform: translateX(-50%); top: 0; font-size: 0.75rem; color: ${dangerColor};">₹${Math.round(spent)}</span>
          <div style="position: absolute; left: ${spentPosition}%; transform: translateX(-50%); top: -4px; height: 4px; width: 2px; background-color: ${dangerColor};"></div>
        `;
      }
      
      thresholdContainer.innerHTML = thresholdHTML;
      budgetCategory.appendChild(thresholdContainer);
      
      // Add final element to DOM
      budgetBars.appendChild(budgetCategory);
      
      // Add delete event listener for the budget
      const deleteBtn = budgetCategory.querySelector('.delete-budget-btn');
      deleteBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const categoryToDelete = e.currentTarget.getAttribute('data-category');
        // Set the budget to 0
        budgets[categoryToDelete] = 0;
        // Re-render budget bars and update stats
        renderBudgetBars();
        updateSummaryStats();
        saveData();
      });
    });
  }
  
  // Save data to localStorage
  function saveData() {
    let userEmail = sessionStorage.getItem("userEmail"); // Get the user email from sessionStorage
    if (userEmail) {
        localStorage.setItem(`${userEmail}_finwiseExpenses`, JSON.stringify(expenses));
        localStorage.setItem(`${userEmail}_finwiseBudgets`, JSON.stringify(budgets));
    } else {
        console.error("User not logged in.");
    }
}

  
  // Load data from localStorage
  function loadData() {
    const userEmail = sessionStorage.getItem("userEmail");
    if (!userEmail) {
        console.error("No user email found in session.");
        return;
    }

    const savedExpenses = localStorage.getItem(`${userEmail}_finwiseExpenses`);
    const savedBudgets = localStorage.getItem(`${userEmail}_finwiseBudgets`);
    
    if (savedExpenses) {
      expenses.push(...JSON.parse(savedExpenses));
    }
    
    if (savedBudgets) {
      const loadedBudgets = JSON.parse(savedBudgets);
      Object.keys(loadedBudgets).forEach(category => {
        budgets[category] = loadedBudgets[category];
      });
    }
}

  
  // Add expense handler
  addExpenseBtn.addEventListener('click', () => {
    const description = document.getElementById('expense-description').value.trim();
    const amount = parseFloat(document.getElementById('expense-amount').value);
    const category = document.getElementById('expense-category').value;
    
    if (!description || isNaN(amount) || amount <= 0) {
      alert('Please enter a valid description and amount.');
      return;
    }
    
    // Add expense
    expenses.push({
      description, 
      amount,
      category,
      date: new Date().toISOString()
    });
    
    // Clear form
    document.getElementById('expense-description').value = '';
    document.getElementById('expense-amount').value = '';
    
    // Update UI
    renderExpenseList();
    renderBudgetBars();
    updateSummaryStats();
    saveData();
  });
  
  // Toggle budget form
  editBudgetBtn.addEventListener('click', () => {
    budgetForm.style.display = budgetForm.style.display === 'none' ? 'block' : 'none';
  });
  
  // Set budget handler
  setBudgetBtn.addEventListener('click', () => {
  const category = document.getElementById('budget-category').value;
  const amount = parseFloat(document.getElementById('budget-amount').value);
  if (isNaN(amount) || amount < 0) {
  alert('Please enter a valid amount.');
  return;
   }
  // Set budget
  budgets[category] = amount;
  // Clear form
  document.getElementById('budget-amount').value = '';
  // Update UI
  renderBudgetBars();
  updateSummaryStats();
  saveData();
   });
  // Initialize
  
  loadData();
  renderExpenseList();
  renderBudgetBars();
  updateSummaryStats();
   });