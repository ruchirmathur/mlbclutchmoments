import React, { useState } from 'react';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import Header from '../components/Header';

const Web: React.FC = () => {

  const [searchResults, setSearchResults] = useState<any>(null);

  const [isLoading, setIsLoading] = useState(false);
  
  const handleSearch = async (query: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`https://{host}/generate?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setSearchResults(data);

    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Header/>
      <Container maxWidth="lg" sx={{ mt: 4, textAlign: 'center' }}>
        <Box sx={{ mb: 4 }}>
          <img src="https://www.mlbstatic.com/team-logos/league-on-dark/1.svg" alt="MLB Logo" height="80" />
        </Box>
        <Typography variant="h4" component="h1" gutterBottom sx={{ color: 'white' }}>
          Search MLB
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
          <SearchBar onSearch={handleSearch} />
        </Box>
        {isLoading ? (
          <CircularProgress sx={{ mt: 4 }} />
        ) : (
          searchResults && <SearchResults results={searchResults} isLoading={isLoading}/>
        )}
      </Container>
    </>
  );
};

export default Web;
