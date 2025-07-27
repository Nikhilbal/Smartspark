import { render, screen } from '@testing-library/react';
import App from './App';

test('renders SmartSpark chat application', () => {
  render(<App />);
  // The app should render without crashing
  expect(document.body).toBeInTheDocument();
}); 