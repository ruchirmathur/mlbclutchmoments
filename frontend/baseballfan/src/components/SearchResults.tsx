import React from 'react';
import { Box, Card, CardContent, Typography, CircularProgress, CardMedia, Link, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

interface SearchResultsProps {
  results: any;
  isLoading: boolean;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, isLoading }) => {
  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!results) {
    return null;
  }

  if (results.game_date) {
    // Game details
    return (
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Game Details
                </Typography>
                <Typography sx={{ mb: 1.5 }} color="text.secondary">
                  {new Date(results.game_date).toLocaleDateString()}
                </Typography>
                <Typography variant="body2">
                  {results.teams.away.name} {results.teams.away.score} - {results.teams.home.name} {results.teams.home.score}
                </Typography>
                <Typography variant="body2">
                  Status: {results.status}
                </Typography>
                <Typography variant="body2">
                  {results.response}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Game Statistics
                </Typography>
                {/* Add game statistics here */}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Clutch Plays
                </Typography>
                {/* Add clutch plays here */}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>Highlights</Typography>
        <Grid container spacing={2}>
          {results.highlights.map((highlight: any, index: number) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card>
                <CardMedia
                  component="video"
                  height="140"
                  src={highlight.video_url}
                  title={highlight.title}
                  controls
                />
                <CardContent>
                  <Typography variant="body2">{highlight.title}</Typography>
                  <Link href="#" onClick={() => console.log('Summarize video')}>
                    Summarize Video
                  </Link>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  } else if (results.leagues) {
    // League details
    return (
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  League Details
                </Typography>
                <Typography variant="body2">
                  {results.response}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  League Information
                </Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Abbreviation</TableCell>
                        <TableCell>Teams</TableCell>
                        <TableCell>Season</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.leagues.map((league: any) => (
                        <TableRow key={league.id}>
                          <TableCell>{league.name}</TableCell>
                          <TableCell>{league.abbreviation}</TableCell>
                          <TableCell>{league.numTeams}</TableCell>
                          <TableCell>{league.season}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  } else if (results.teams) {
    // Team details
    return (
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Team Summary
                </Typography>
                <Typography variant="body2">
                  {results.response}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Team Information
                </Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Logo</TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell>League</TableCell>
                        <TableCell>Division</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.teams.map((team: any) => (
                        <TableRow key={team.id}>
                          <TableCell>
                            <img src={team.teamurl} alt={team.name} style={{ width: 30, height: 30 }} />
                          </TableCell>
                          <TableCell>{team.name}</TableCell>
                          <TableCell>{team.league.name}</TableCell>
                          <TableCell>{team.division.name}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  }

  return null;
};

export default SearchResults;
