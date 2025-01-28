// src/components/AudioIcon.tsx
import React, { useState, useRef } from 'react';
import { IconButton } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';

const AudioIcon: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const websocketRef = useRef<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const sourceNodeRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const processorNodeRef = useRef<ScriptProcessorNode | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContextRef.current = new AudioContext();
      sourceNodeRef.current = audioContextRef.current.createMediaStreamSource(stream);
      processorNodeRef.current = audioContextRef.current.createScriptProcessor(4096, 1, 1);

      sourceNodeRef.current.connect(processorNodeRef.current);
      processorNodeRef.current.connect(audioContextRef.current.destination);

      websocketRef.current = new WebSocket('ws://localhost:9082');
      websocketRef.current.onopen = () => {
        console.log('WebSocket connection established');
        setIsRecording(true);
      };

      processorNodeRef.current.onaudioprocess = (e) => {
        if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
          const pcmData = e.inputBuffer.getChannelData(0);
          websocketRef.current.send(pcmData);
        }
      };
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (processorNodeRef.current) {
      processorNodeRef.current.disconnect();
    }
    if (sourceNodeRef.current) {
      sourceNodeRef.current.disconnect();
    }
    if (websocketRef.current) {
      websocketRef.current.close();
    }
    setIsRecording(false);
  };

  const handleClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <IconButton onClick={handleClick} sx={{ ml: 1, color: 'white' }}>
      <MicIcon />
    </IconButton>
  );
};

export default AudioIcon;
