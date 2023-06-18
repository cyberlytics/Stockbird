import React from 'react';
import { useNavigate } from 'react-router-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Home from '../pages/Home';

describe('Home', () => {
  it('should make API call when OK button is clicked', () => {

    // renders the Home component
    render(<Home />);

    // simulates typing something in the input field
    const input = screen.getByPlaceholderText('Search stocks by symbol (e. g. AAPL)');
    userEvent.type(input, 'AAPL');

    // simulates clicking the OK button
    const okButton = screen.getByRole('button', { name: 'OK' });
    fireEvent.click(okButton);

    // tests if the API is called with the correct parameters
    expect(global.fetch).toHaveBeenCalledWith('https://szlw5m95d9.execute-api.eu-central-1.amazonaws.com/dev', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ control: '_get_stock_data', symbol: 'AAPL' }),
      redirect: 'follow',
    });

  });
});
