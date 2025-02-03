import React from 'react';
import {
  TableContainer,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography,
  TableHead,
  styled,
} from '@mui/material';

interface HotColdZone {
  color: string;
  temp: string;
  value: string;
  zone: string;
}

interface Stat {
  name: string;
  zones: HotColdZone[];
}

interface StatGroup {
  group: { displayName: string };
  splits: { stat: Stat }[];
}

interface PitchData {
  breaks: {
    breakAngle: number;
    breakHorizontal: number;
    breakLength: number;
    breakVertical: number;
    breakVerticalInduced: number;
    breakY: number;
    spinDirection: number;
    spinRate: number;
  };
  coordinates: {
    aX: number;
    aY: number;
    aZ: number;
    pX: number;
    pZ: number;
    pfxX: number;
    pfxZ: number;
    vX0: number;
    vY0: number;
    vZ0: number;
    x: number;
    x0: number;
    y: number;
    y0: number;
    z0: number;
  };
  endSpeed: number;
  extension: number;
  plateTime: number;
  startSpeed: number;
  strikeZoneBottom: number;
  strikeZoneTop: number;
  typeConfidence: number;
  zone: number;
}

interface Details {
  ballColor?: string; // Optional because not always present
  call: { code: string; description: string };
  code: string;
  description: string;
  hasReview: boolean;
  isBall: boolean;
  isInPlay: boolean;
  isOut: boolean;
  isStrike: boolean;
  trailColor?: string; // Optional
  type: { code: string; description: string };
}

interface HitData {
  coordinates: { coordX: number; coordY: number };
  hardness: string;
  launchAngle: number;
  launchSpeed: number;
  location: string;
  totalDistance: number;
  trajectory: string;
}

interface PitchEvent {
  count: { balls: number; outs: number; strikes: number };
  details: Details;
  endTime: string;
  hitData?: HitData; // Optional because not always present
  index: number;
  isPitch: boolean;
  pitchData: PitchData;
  pitchNumber: number;
  playId: string;
  startTime: string;
  type: string;
}

interface Credit {
  credit: string;
  player: { id: number; link: string };
  position: {
    abbreviation: string;
    code: string;
    name: string;
    type: string;
  };
}

interface RunnerDetails {
  earned: boolean;
  event: string;
  eventType: string;
  isScoringEvent?: boolean; // Optional
  movementReason: string | null;
  playIndex: number;
  rbi: boolean;
  responsiblePitcher: string | null;
  runner: { fullName: string; id: number; link: string };
  teamUnearned: boolean;
}

interface Movement {
  end: string | null;
  isOut: boolean;
  originBase: string | null;
  outBase: string;
  outNumber: number;
  start: string | null;
}

interface Runner {
  credits: Credit[];
  details: RunnerDetails;
  movement: Movement;
}

interface Result {
    awayScore: number;
    description: string;
    event: string;
    eventType: string;
    homeScore: number;
    isOut: boolean;
    rbi: number;
    type: string;
}

interface GameData {
  about: {
    atBatIndex: number;
    captivatingIndex: number;
    endTime: string;
    halfInning: string;
    hasOut: boolean;
    hasReview: boolean;
    inning: number;
    isComplete: boolean;
    isScoringPlay: boolean;
    isTopInning: boolean;
    startTime: string;
  };
  actionIndex: number[];
  atBatIndex: number;
  count: { balls: number; outs: number; strikes: number };
  matchup: {
    batSide: { code: string; description: string };
    batter: { fullName: string; id: number; link: string };
    batterHotColdZoneStats: { stats: StatGroup[] };
    batterHotColdZones: HotColdZone[];
    pitchHand: { code: string; description: string };
    pitcher: { fullName: string; id: number; link: string };
    pitcherHotColdZones: any[]; // Adjust type as needed
    splits: { batter: string; menOnBase: string; pitcher: string };
  };
  pitchIndex: number[];
  playEndTime: string;
  playEvents: PitchEvent[];
  result: Result;
  runnerIndex: number[];
  runners: Runner[];
  summary: string;
}

// Styled Components for theming
const StyledTableCell = styled(TableCell)(({ theme }) => ({
    fontWeight: 'bold',
    backgroundColor: theme.palette.grey[200], // Light gray for headers
    color: theme.palette.text.primary, // Use theme text color
  }));
  
  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover, // Subtle background for odd rows
    },
    '&:hover': {
      backgroundColor: theme.palette.action.selected, // Highlight on hover
    },
  }));
  const TitleTypography = styled(Typography)(({ theme }) => ({
    padding: theme.spacing(2),
    fontWeight: 'bold',
    color: theme.palette.text.primary, // Use theme text color
  }));
  
  
  const CurrentPlay: React.FC<{ data: GameData | null }> = ({ data }) => {
    if (!data) {
      return <p>No game data available.</p>;
    }
  
    const renderHotColdZones = (zones: HotColdZone[]) => (
      <TableCell>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Zone</TableCell>
              <TableCell>Temp</TableCell>
              <TableCell>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {zones.map((zoneData, index) => (
              <TableRow key={index}>
                <TableCell>{zoneData.zone}</TableCell>
                <TableCell>{zoneData.temp}</TableCell>
                <TableCell>{zoneData.value}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableCell>
    );
  
    const renderStats = (stats: StatGroup[]) => (
      <TableCell>
        {stats.map((statGroup, groupIndex) => (
          <div key={groupIndex}>
            <Typography variant="subtitle1">{statGroup.group.displayName}</Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Stat</TableCell>
                  <TableCell>Zones</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {statGroup.splits.map((split, splitIndex) => (
                  <TableRow key={splitIndex}>
                    <TableCell>{split.stat.name}</TableCell>
                    {renderHotColdZones(split.stat.zones)}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ))}
      </TableCell>
    );
  
    const renderPitchData = (pitch: PitchEvent) => (
        <StyledTableRow>
          <TableCell>{pitch.pitchNumber}</TableCell>
          <TableCell>{pitch.details?.type?.description || "N/A"}</TableCell> 
          <TableCell>{pitch.details?.call?.description || "N/A"}</TableCell> 
          <TableCell>{pitch.pitchData.startSpeed}</TableCell>
          <TableCell>{pitch.pitchData.endSpeed}</TableCell>
          {pitch.hitData && (
            <>
              <TableCell>{pitch.hitData.launchSpeed}</TableCell>
              <TableCell>{pitch.hitData.launchAngle}</TableCell>
              <TableCell>{pitch.hitData.trajectory}</TableCell>
              <TableCell>{pitch.hitData.totalDistance}</TableCell>
            </>
          )}
        </StyledTableRow>
      );
      
  
    const renderRunner = (runner: Runner) => (
      <StyledTableRow> {/* Use styled component here */}
        <TableCell>{runner.details.runner.fullName}</TableCell>
        <TableCell>{runner.details.event}</TableCell>
        <TableCell>{runner.movement.outBase || "N/A"}</TableCell>
        <TableCell>{runner.movement.isOut ? "Out" : "Safe"}</TableCell>
      </StyledTableRow>
    );
  
    return (
      <TableContainer component={Paper} sx={{ borderRadius: '8px', overflow: 'hidden' }}>
          
          <Typography variant="h5" gutterBottom component="div" sx={{ p: 2,  backgroundColor: '#3f51b5', color: 'white' }}>
          Summary
        </Typography>
        <Table>
          <TableBody>
            <StyledTableRow>
              <TableCell>{data?.summary}</TableCell>
            </StyledTableRow>
          </TableBody>
        </Table>
        <Typography variant="h5" gutterBottom component="div" sx={{ p: 2, backgroundColor: '#3f51b5', color: 'white' }}>
          Game Information
        </Typography>
        <Table>
          <TableBody>
            <StyledTableRow>
              <StyledTableCell><strong>Start Time</strong></StyledTableCell>
              <TableCell>{data ? new Date(data.about.startTime).toLocaleString() : "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>End Time</strong></StyledTableCell>
              <TableCell>{data ? new Date(data.about.endTime).toLocaleString() : "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Inning</strong></StyledTableCell>
              <TableCell>{data?.about.inning || "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Home Score</strong></StyledTableCell>
              <TableCell>{data?.result.homeScore || "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Away Score</strong></StyledTableCell>
              <TableCell>{data?.result.awayScore || "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Batter</strong></StyledTableCell>
              <TableCell>{data?.matchup.batter.fullName || "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Pitcher</strong></StyledTableCell>
              <TableCell>{data?.matchup.pitcher.fullName || "N/A"}</TableCell>
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Batter Hot/Cold Zones</strong></StyledTableCell>
              {data?.matchup.batterHotColdZones && renderHotColdZones(data.matchup.batterHotColdZones)}
            </StyledTableRow>
            <StyledTableRow>
              <StyledTableCell><strong>Batter Hot/Cold Zone Stats</strong></StyledTableCell>
              {data?.matchup.batterHotColdZoneStats?.stats && renderStats(data.matchup.batterHotColdZoneStats.stats)}
            </StyledTableRow>
          </TableBody>
        </Table>
  
        <Typography variant="h5" gutterBottom component="div" sx={{ p: 2, mt: 2, backgroundColor: '#3f51b5', color: 'white' }}>
          Play Events
        </Typography>
        <Table>
          <TableHead>
            <StyledTableRow>
              <StyledTableCell>Pitch #</StyledTableCell>
              <StyledTableCell>Pitch Type</StyledTableCell>
              <StyledTableCell>Call</StyledTableCell>
              <StyledTableCell>Start Speed</StyledTableCell>
              <StyledTableCell>End Speed</StyledTableCell>
              <StyledTableCell>Launch Speed</StyledTableCell>
              <StyledTableCell>Launch Angle</StyledTableCell>
              <StyledTableCell>Trajectory</StyledTableCell>
              <StyledTableCell>Distance</StyledTableCell>
            </StyledTableRow>
          </TableHead>
          <TableBody>
            {data?.playEvents?.filter((event) => event.isPitch).map(renderPitchData)}
          </TableBody>
        </Table>
  
        <Typography variant="h5" gutterBottom component="div" sx={{ p: 2, mt: 2, backgroundColor: '#3f51b5', color: 'white' }}>
          Runners
        </Typography>
        <Table>
          <TableHead>
            <StyledTableRow>
              <StyledTableCell>Runner</StyledTableCell>
              <StyledTableCell>Event</StyledTableCell>
              <StyledTableCell>Out Base</StyledTableCell>
              <StyledTableCell>Result</StyledTableCell>
            </StyledTableRow>
          </TableHead>
          <TableBody>
            {data?.runners?.map(renderRunner)}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

export default CurrentPlay;