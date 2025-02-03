import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

interface SummaryPopupProps {
    isOpen: boolean;
    summary: string;
    title: string;
    onClose: () => void;
  }
  const SummaryPopup: React.FC<SummaryPopupProps> = ({ isOpen, summary, title, onClose }) => {
    return (
      <Dialog open={isOpen} onClose={onClose}>
        <DialogTitle>{title}</DialogTitle>
        <DialogContent>
          <Typography>{summary}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Close</Button>
        </DialogActions>
      </Dialog>
    );
  };

export default SummaryPopup;
