import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'dark' | 'light';
type FontSize = 'sm' | 'base' | 'lg';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  fontSize: FontSize;
  setFontSize: (size: FontSize) => void;
  highContrast: boolean;
  toggleHighContrast: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem('healix_theme');
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  });

  const [fontSize, setFontSizeState] = useState<FontSize>(() => {
    const saved = localStorage.getItem('healix_font_size');
    if (saved === 'sm' || saved === 'base' || saved === 'lg') return saved;
    return 'base';
  });

  const [highContrast, setHighContrast] = useState<boolean>(() => {
    return localStorage.getItem('healix_high_contrast') === 'true';
  });

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('dark', 'light');
    root.classList.add(theme);
    localStorage.setItem('healix_theme', theme);
  }, [theme]);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('font-scale-sm', 'font-scale-base', 'font-scale-lg');
    root.classList.add(`font-scale-${fontSize}`);
    localStorage.setItem('healix_font_size', fontSize);
  }, [fontSize]);

  useEffect(() => {
    const root = document.documentElement;
    if (highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
    localStorage.setItem('healix_high_contrast', String(highContrast));
  }, [highContrast]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const setFontSize = (size: FontSize) => {
    setFontSizeState(size);
  };

  const toggleHighContrast = () => {
    setHighContrast(prev => !prev);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, fontSize, setFontSize, highContrast, toggleHighContrast }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within a ThemeProvider');
  return ctx;
};

