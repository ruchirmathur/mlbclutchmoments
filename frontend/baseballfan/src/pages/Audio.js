import React, { useState, useEffect, useRef } from 'react';
import MicIcon from '@mui/icons-material/Mic';
import { IconButton } from '@mui/material';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Grid,
  Paper,
  ThemeProvider,
  createTheme,
  Box,
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  CardMedia
} from '@mui/material';
import AudioVisualizer from './AudioVisualizer';
import AudioPlayer from './AudioPlayer';
import CurrentPlay from '../components/CurrentPlay';

const theme = createTheme({
  palette: {
    primary: {
      main: '#00264D',
    },
    secondary: {
      main: '#E31837',
    },
  },
});

const WS_URL = "";

const Audio = ({}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [wsStatus, setWsStatus] = useState('disconnected');
  const [inputVisualizerSource, setInputVisualizerSource] = useState(null);
  const [audioOutput, setAudioOutput] = useState(null);
  const webSocketRef = useRef(null);
  const audioContextRef = useRef(null);
  const processorRef = useRef(null);
  const pcmDataRef = useRef([]);
  const intervalRef = useRef(null);
  const audioInputContextRef = useRef(null);
  const workletNodeRef = useRef(null);
  const [seasonData, setSeasonData] = useState(null);
  const [leagueData, setLeagueData] = useState(null);
  const [rosterData, setRosterData] = useState(null);
  const [teamData, setTeamData] = useState(null);
  const [gameData, setGameData] = useState(null);
  const [playData, setPlayData] = useState(null);
  const [currentplayData, setCurrentPlayData] = useState(null);

  useEffect(() => {
    let reconnectTimeout;

    const setupWebSocket = () => {
      if (webSocketRef.current) {
        webSocketRef.current.close();
      }
      initializeWebSocket();
    };

    setupWebSocket();

    return () => {
      if (webSocketRef.current) {
        webSocketRef.current.close();
      }
      clearTimeout(reconnectTimeout);
      stopAudioRecording();
    };
  }, []);

  const initializeWebSocket = () => {
    console.log("Connecting to WebSocket:", WS_URL);
    const ws = new WebSocket(WS_URL);

    ws.onclose = (event) => {
      console.log("WebSocket closed:", event);
      setWsStatus('disconnected');
      setTimeout(() => initializeWebSocket(), 5000);
    };

    ws.onerror = (event) => {
      console.log("WebSocket error:", event);
      setWsStatus('error');
      ws.close();
    };

    ws.onopen = (event) => {
      console.log("WebSocket open:", event);
      setWsStatus('connected');
      sendSetupMessage(ws);
    };

    ws.onmessage = handleIncomingMessage;

    webSocketRef.current = ws;
  };

  const sendSetupMessage = (ws) => {
    console.log("Sending setup message");
    const setupMessage = {
      setup: { generation_config: { response_modalities: ["AUDIO"] } },
    };
    ws.send(JSON.stringify(setupMessage));
  };

  const sendAudioMessage = (b64PCM) => {
    if (!webSocketRef.current || webSocketRef.current.readyState !== WebSocket.OPEN) {
      console.log("WebSocket not ready");
      return;
    }

    const payload = {
      realtime_input: {
        media_chunks: [
          { mime_type: "audio/pcm", data: b64PCM },
        ],
      },
    };

    webSocketRef.current.send(JSON.stringify(payload));
    console.log("Sent audio data");
  };

  const handleIncomingMessage = (event) => {
    const messageData = JSON.parse(event.data);
    const response = new Response(messageData);

    if (response.text) {

      const mlbResponse = JSON.parse(response.text)

      if (mlbResponse[0].name === "get_mlb_seasons") {
        // Check if the response contains season data
        try {

          if (mlbResponse[0].response && mlbResponse[0].response.result) {
            const seasons = JSON.parse(mlbResponse[0].response.result).seasons;
            setSeasonData(seasons[0]); // Assuming we want the first season
          }
        } catch (error) {
          console.error("Error parsing season data:", error);
        }
      }
      if (mlbResponse[0].name === "get_mlb_leagues") {
        try {
          if (mlbResponse[0].response && mlbResponse[0].response.result) {
            const leagues = JSON.parse(mlbResponse[0].response.result).leagues;
            setLeagueData(leagues);
          }
        } catch (error) {
          console.error("Error parsing league data:", error);
        }
      }
      if (mlbResponse[0].name === "get_mlb_teams") {
        try {
          if (mlbResponse[0].response && mlbResponse[0].response.result) {
            const teams = JSON.parse(mlbResponse[0].response.result).teams;
            setTeamData(teams);
          }
        } catch (error) {
          console.error("Error parsing team data:", error);
        }
      }
      if (mlbResponse[0].name === "get_mlb_roster") {
        try {
          if (mlbResponse[0].response && mlbResponse[0].response.result) {
            const roster = JSON.parse(mlbResponse[0].response.result).roster;
            setRosterData(roster);
          }
        } catch (error) {
          console.error("Error parsing roster data:", error);
        }
      }
      if (mlbResponse[0].name === "get_game_data") {
        try {
          if (mlbResponse[0].response && mlbResponse[0].response.result) {
            const games = JSON.parse(mlbResponse[0].response.result);
            console.log("test the games" + games.teams.away.name);
            setGameData(games);
          }
        } catch (error) {
          console.error("Error parsing game data:", error);
        }
      }
      if (mlbResponse[0].name === "get_mlb_clutch_plays") {
        try {
          if (mlbResponse[0].response.result) {
            const plays = JSON.parse(mlbResponse[0].response.result);
            setPlayData(plays);
          }
        } catch (error) {
          console.error("Error parsing clutch plays data:", error);
        }
      }  
      if (mlbResponse[0].name === "get_current_play") {
        try {
          if (mlbResponse[0].response.result) {
            console.log("test the current" + mlbResponse[0].response.result);
            const currentplays = JSON.parse(mlbResponse[0].response);
            setCurrentPlayData(currentplays);
          }
        } catch (error) {
          console.error("Error parsing current plays data:", error);
        }
      }
    }
    if (response.audioData) {
      processAudioResponse(response.audioData);
    }
  };


  const initAudioContext = async () => {
    if (audioInputContextRef.current) return;

    audioInputContextRef.current = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
    await audioInputContextRef.current.audioWorklet.addModule("pcm-processor.js");
    workletNodeRef.current = new AudioWorkletNode(audioInputContextRef.current, "pcm-processor");
    workletNodeRef.current.connect(audioInputContextRef.current.destination);
  };

  const processAudioResponse = async (base64AudioChunk) => {
    try {
      if (!audioInputContextRef.current) {
        await initAudioContext();
      }

      if (audioInputContextRef.current.state === "suspended") {
        await audioInputContextRef.current.resume();
      }

      const arrayBuffer = base64ToArrayBuffer(base64AudioChunk);
      const float32Data = convertPCM16LEToFloat32(arrayBuffer);
      workletNodeRef.current.port.postMessage(float32Data);

      const bufferSource = audioInputContextRef.current.createBufferSource();
      const audioBuffer = audioInputContextRef.current.createBuffer(1, float32Data.length, 24000);
      audioBuffer.getChannelData(0).set(float32Data);
      bufferSource.buffer = audioBuffer;

    } catch (error) {
      console.error("Error processing audio chunk:", error);
    }
  };

  const recordAudioChunk = () => {
    const buffer = new ArrayBuffer(pcmDataRef.current.length * 2);
    const view = new DataView(buffer);
    pcmDataRef.current.forEach((value, index) => {
      view.setInt16(index * 2, value, true);
    });
    const base64 = btoa(String.fromCharCode.apply(null, new Uint8Array(buffer)));
    sendAudioMessage(base64);
    pcmDataRef.current = [];
  };

  const startAudioRecording = async () => {
    try {
      audioContextRef.current = new AudioContext({ sampleRate: 16000 });

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { channelCount: 1, sampleRate: 16000 },
      });

      const source = audioContextRef.current.createMediaStreamSource(stream);
      processorRef.current = audioContextRef.current.createScriptProcessor(4096, 1, 1);
      setInputVisualizerSource(source);

      processorRef.current.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        const pcm16 = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          pcm16[i] = inputData[i] * 0x7fff;
        }
        pcmDataRef.current.push(...pcm16);
      };

      source.connect(processorRef.current);
      processorRef.current.connect(audioContextRef.current.destination);

      intervalRef.current = setInterval(recordAudioChunk, 2000);
      setIsRecording(true);
    } catch (error) {
      console.error("Error starting audio recording:", error);
      setIsRecording(false);
    }
  };

  const stopAudioRecording = () => {
    if (processorRef.current) {
      processorRef.current.disconnect();
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    clearInterval(intervalRef.current);
    setIsRecording(false);
  };

  const SeasonDataTable = ({ data }) => {
    if (!data || data.length === 0) {
      return <p>No season data available.</p>;
    }

    return (
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Field</TableCell>
              <TableCell>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.entries(data).map(([key, value]) => (
              <TableRow key={key}>
                <TableCell>{key}</TableCell>
                <TableCell>{value.toString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  const LeagueDataTable = ({ data }) => {
    if (!data || data.length === 0) {
      return <p>No league data available.</p>;
    }

    return (
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>League Name</TableCell>
              <TableCell>Abbreviation</TableCell>
              <TableCell>Number of Teams</TableCell>
              <TableCell>Season State</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((league) => (
              <TableRow key={league.id}>
                <TableCell>{league.name ?? 'N/A'}</TableCell>
                <TableCell>{league.abbreviation ?? 'N/A'}</TableCell>
                <TableCell>{league.numTeams ?? 'N/A'}</TableCell>
                <TableCell>{league.seasonState ?? 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };
  const RosterDataTable = ({ data }) => {
    if (!data || data.length === 0) {
      return <p>No roster data available.</p>;
    }
    return (
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Position</TableCell>
              <TableCell>Jersey Number</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((player) => (
              <TableRow key={player.person.id ?? 'N/A'}>
                <TableCell>{player.person.fullName ?? 'N/A'}</TableCell>
                <TableCell>{player.position.name ?? 'N/A'}</TableCell>
                <TableCell>{player.jerseyNumber ?? 'N/A'}</TableCell>
                <TableCell>{player.status.description ?? 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };
  const TeamDataTable = ({ data }) => {
    if (!data || data.length === 0) {
      return <p>No team data available.</p>;
    }

    return (
      <TableContainer component={Paper}>
        <Table aria-label="MLB Team Data Table">
          <TableHead>
            <TableRow>
              <TableCell>Team Name</TableCell>
              <TableCell>Abbreviation</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>League</TableCell>
              <TableCell>First Year of Play</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((data) => (
              <TableRow key={data.id}>
                <TableCell>{data.name ?? 'N/A'}</TableCell>
                <TableCell>{data.abbreviation ?? 'N/A'}</TableCell>
                <TableCell>{data.locationName ?? 'N/A'}</TableCell>
                <TableCell>{data.league.name ?? 'N/A'}</TableCell>
                <TableCell>{data.firstYearOfPlay ?? 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };
  const GameInfoTable = ({ data }) => {


    if (!data || data.length === 0) {
      return <p>No game data available.</p>;
    }
    const { game_date, status, teams, highlights } = data;

    return (
      <TableContainer component={Paper}>
        <Typography variant="h6" gutterBottom component="div" sx={{ p: 2 }}>
          Game Information
        </Typography>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell><strong>Date</strong></TableCell>
              <TableCell>{new Date(game_date).toLocaleString()}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><strong>Status</strong></TableCell>
              <TableCell>{status ?? 'N/A'}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><strong>Away Team</strong></TableCell>
              <TableCell>{teams.away.name ?? 'N/A'} - {teams.away.score ?? 'N/A'}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><strong>Home Team</strong></TableCell>
              <TableCell>{teams.home.name ?? 'N/A'} - {teams.home.score ?? 'N/A'}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <Typography variant="h6" gutterBottom component="div" sx={{ p: 2, mt: 2 }}>
          Highlights
        </Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Video</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {highlights && highlights.map((highlight) => (
              <TableRow key={highlight.id}>
                <TableCell>{highlight.title ?? 'N/A'}</TableCell>
                <TableCell>
                  <CardMedia
                    component="video"
                    height="140"
                    src={highlight.video_url ?? 'N/A'}
                    title={highlight.title ?? 'N/A'}
                    controls
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };
  const PlayHighlights = ({ data }) => {
    if (!data || data.length === 0) {
      return <p>No play data available.</p>;
    }
    const gameInfo = data.game_info;
    const keyPlays = data.key_plays;

    return (
      <Box sx={{ margin: 2 }}>
        <Typography variant="h4" gutterBottom>
          Game Highlights
        </Typography>

        <Typography variant="h6" gutterBottom>
          {gameInfo.away_team} ({gameInfo.away_score}) @ {gameInfo.home_team} ({gameInfo.home_score})
        </Typography>

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="game highlights table">
            <TableHead>
              <TableRow>
                <TableCell>Inning</TableCell>
                <TableCell>Event</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Batter</TableCell>
                <TableCell>Pitcher</TableCell>
                <TableCell>Pitch Speed</TableCell>
                <TableCell>Video</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {keyPlays.map((play) => (
                <TableRow
                  key={play.play_id}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell>{`${play.is_top_inning ? 'Top' : 'Bottom'} ${play.inning}`}</TableCell>
                  <TableCell>{play.event ?? 'N/A'}</TableCell>
                  <TableCell>{play.description ?? 'N/A'}</TableCell>
                  <TableCell>{play.batter ?? 'N/A'}</TableCell>
                  <TableCell>{play.pitcher ?? 'N/A'}</TableCell>
                  <TableCell>{`${play.pitch_data.start_speed ?? 'N/A'} mph`}</TableCell>
                  <TableCell>
                    {play.video_url && (
                      <CardMedia
                        component="video"
                        src={play.video_url ?? 'N/A'}
                        controls
                      />
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    );
  };
  const handleClick = () => {
    if (isRecording) {
      stopAudioRecording();
    } else {
      startAudioRecording();
    }
  };
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
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
        <Container maxWidth="lg" sx={{ mt: 4, textAlign: 'center' }}>
          <Box sx={{ mb: 4 }}>
            <img src="https://www.mlbstatic.com/team-logos/league-on-dark/1.svg" alt="MLB Logo" height="80" />
          </Box>
          <Box sx={{ mb: 4 }}>
            <IconButton onClick={isRecording ? stopAudioRecording : startAudioRecording} sx={{ ml: 1, color: 'white' }}>
              <MicIcon />
            </IconButton>
            <Typography variant="h6" gutterBottom>Please click on the audio icon to start</Typography>
          </Box>
          <Grid container spacing={3} justifyContent="center">
            <Grid item xs={12} md={6}>
              <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom>You can ask me a Baseball Question</Typography>
                <AudioVisualizer audioContext={audioContextRef.current} sourceNode={inputVisualizerSource} />
              </Paper>
            </Grid>
            {(seasonData || leagueData || rosterData || teamData || gameData || currentplayData) && (
              <Grid item xs={12}>
                <Paper elevation={3} sx={{ p: 2 }}>
                  {seasonData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Seasons</Typography>
                      <SeasonDataTable data={seasonData} />
                    </>
                  )}
                  {leagueData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Leagues</Typography>
                      <LeagueDataTable data={leagueData} />
                    </>
                  )}
                  {rosterData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Team Roster</Typography>
                      <RosterDataTable data={rosterData} />
                    </>
                  )}
                  {teamData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Teams</Typography>
                      <TeamDataTable data={teamData} />
                    </>
                  )}
                  {gameData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Games</Typography>
                      <GameInfoTable data={gameData} />
                    </>
                  )}
                  {playData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Games</Typography>
                      <PlayHighlights data={playData} />
                    </>
                  )}
                  {currentplayData && (
                    <>
                      <Typography variant="h6" gutterBottom>MLB Games</Typography>
                      <CurrentPlay data={currentplayData} />
                    </>
                  )}
                </Paper>
              </Grid>
            )}
            {audioOutput && (
              <Grid item xs={12}>
                <AudioPlayer audioSrc={audioOutput} />
              </Grid>
            )}
          </Grid>

        </Container>
      </Box>
    </ThemeProvider>
  );
};
class Response {
  constructor(data) {
    this.text = data.text || null;
    this.audioData = data.audio || null;
    this.endOfTurn = data.endOfTurn || null;
  }
}

function base64ToArrayBuffer(base64) {
  const binaryString = window.atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

function convertPCM16LEToFloat32(pcmData) {
  const inputArray = new Int16Array(pcmData);
  const float32Array = new Float32Array(inputArray.length);
  for (let i = 0; i < inputArray.length; i++) {
    float32Array[i] = inputArray[i] / 32768;
  }
  return float32Array;
}

export default Audio;

