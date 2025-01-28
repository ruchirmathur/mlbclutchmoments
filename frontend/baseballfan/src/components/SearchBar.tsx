// src/components/SearchBar.tsx
import React, { useState } from 'react';
import { Autocomplete, TextField, InputAdornment, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AudioIcon from './AudioIcon';

const suggestions = [
  'Whats the post season start date in 1919 ?',
  'Whats All start date in 2009?',
  'How many MLB leagues were there in 2022 season ?',
  'How many MLB teams were there in American league in 2010 season ?',
  'What was the post season start date in National League and American League in 1966 ?',
  'How many number of games were there on National league in 1976 ?',
  'Give me details you have for American league in 2023 ?',
  'Give me details you have for National league in 2023 ?',
  'List all the MLB team that were part of the National league in 2022 ?',
  'What is the venue name for the team Boston Red Sox in 1998?',
  'Give me information on New York Yankees from the 2010 season',
  'Give me information on Boston Red Sox from the 2010 season',
  'Mike Trout',
  'MLB All-Star Game',
  'World Series 2025',
  'give details for the SF giants game on 2024-03-28',
];

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [value, setValue] = useState<string | null>(null);

  const handleSearch = (event: React.SyntheticEvent, newValue: string | null) => {
    if (newValue) {
      setValue(newValue);
      onSearch(newValue);
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', maxWidth: 800, margin: 'auto' }}>
      <Autocomplete
        freeSolo
        options={suggestions}
        renderInput={(params) => (
          <TextField
            {...params}
            placeholder="Search MLB leagues, teams, players, schedules, statistics and venues"
            variant="outlined"
            fullWidth
            InputProps={{
              ...params.InputProps,
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{
              backgroundColor: 'white',
              borderRadius: 1,
              '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  borderColor: 'white',
                },
              },
              '& .MuiInputBase-input': {
                fontSize: '1.2rem',
                padding: '15px 14px',
              },
            }}
          />
        )}
        value={value}
        onChange={handleSearch}
        sx={{
          width: '100%',
          '& .MuiAutocomplete-inputRoot': {
            padding: '2px 4px',
            display: 'flex',
            alignItems: 'center',
            width: '100%',
          },
        }}
      />
      <AudioIcon />
    </Box>
  );
};

export default SearchBar;
