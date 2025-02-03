import React, { useState } from 'react';
import { AppBar, Toolbar, Typography} from '@mui/material';


const Header: React.FC = ({ }) => {
  return (
    <AppBar position="static" sx={{ backgroundColor: '#001C48' }}>
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            textAlign: 'center'
          }}
        >
          MLB Clutch Moments
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
