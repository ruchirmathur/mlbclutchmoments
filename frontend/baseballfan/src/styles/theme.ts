// src/styles/theme.ts
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#002D72', // MLB blue color
    },
    background: {
      default: '#002D72',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#002D72',
          color: '#ffffff',
        },
      },
    },
  },
});

export default theme;
