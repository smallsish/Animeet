// src/components/Header.test.tsx
import { render, screen } from '@testing-library/react';
import Header from './Header';

test('renders the Header component', () => {
  render(<Header />);
  const headerElement = screen.getByText(/My Basic Next.js 15 TypeScript App/i);
  expect(headerElement).toBeInTheDocument();
});
