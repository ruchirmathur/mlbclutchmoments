import React, { useState} from 'react';
import { Box, Card, CardContent, Typography, CircularProgress, CardMedia, Link, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import SummaryPopup from './SummaryPopup';
import CurrentPlay from './CurrentPlay';

interface SearchResultsProps {
  results: any;
  isLoading: boolean;
}


const SearchResults: React.FC<SearchResultsProps> = ({ results, isLoading }) => {
  const [popupState, setPopupState] = useState({
    isOpen: false,
    summary: '',
    title: ''
  });
  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  const handleSummarizeVideo = async (videoUrl: string | number | boolean, title: any) => {
    try {
      const response = await fetch(`{hostname}/generateVideoSummary?query=${encodeURIComponent(videoUrl)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch summary');
      }
      const data = await response.json();

      setPopupState({ isOpen: true, summary: data.summary, title: title });
    } catch (error) {
      console.error('Error summarizing video:', error);
      setPopupState({ isOpen: true, summary: 'Failed to summarize video.', title: title });
    }
  };

  if (!results) {
    return null;
  }
  if (results && results.about) {
    return (
      <div>
        <CurrentPlay data={results} />
      </div>
    );
  }
  if (results.game_date) {
    // Game details
    return (
      <Box sx={{ mt: 8 }}>
        <Grid container justifyContent="center" spacing={2}>
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
        </Grid>
        <Typography variant="h5" sx={{ mt: 4, mb: 2, textAlign: 'center' }}>Highlights</Typography>
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
                  <Link
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      handleSummarizeVideo(highlight.video_url, highlight.title);
                    }}
                  >
                    Summarize Video
                  </Link>
                  <SummaryPopup
                    isOpen={popupState.isOpen}
                    summary={popupState.summary}
                    title={popupState.title}
                    onClose={() => setPopupState({ ...popupState, isOpen: false })}
                  />
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
                  {results.summary}
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
                  {results.summary}
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
  else if (results.seasons) {
    // League details
    return (
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Season Details
                </Typography>
                <Typography variant="body2">
                  {results.summary}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  Season Information
                </Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Offseason Start</TableCell>
                        <TableCell>Offseason End</TableCell>
                        <TableCell>RegularSeason Start</TableCell>
                        <TableCell>RegularSeason End </TableCell>
                        <TableCell>PostSeason Start</TableCell>
                        <TableCell>PostSeason End</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.seasons.map((season: any) => (
                        <TableRow key={season.id}>
                          <TableCell>{season.offseasonStartDate}</TableCell>
                          <TableCell>{season.offSeasonEndDate}</TableCell>
                          <TableCell>{season.regularSeasonStartDate}</TableCell>
                          <TableCell>{season.regularSeasonEndDate}</TableCell>
                          <TableCell>{season.postSeasonStartDate}</TableCell>
                          <TableCell>{season.postSeasonEndDate}</TableCell>
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
  else if (results.roster) {
    // League details
    return (
      <Card>
        <CardContent>
          <Typography variant="h5" component="div" gutterBottom>
            {results.roster.rosterType} Roster
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            {results.summary}
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Player</TableCell>
                  <TableCell>Jersey Number</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Position</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {results.roster.map((player: any) => (
                  <TableRow key={player.person.id}>
                    <TableCell>
                      <img src={player.playerurl} alt={player.person.fullName} style={{ width: 50, height: 50 }} />
                    </TableCell>
                    <TableCell>{player.jerseyNumber || 'N/A'}</TableCell>
                    <TableCell>{player.person.fullName}</TableCell>
                    <TableCell>{player.position.name}</TableCell>
                    <TableCell>{player.status.description}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    );
  }
  return null;
};

export default SearchResults;
