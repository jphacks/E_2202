import * as React from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function Search() {
  const [os, setOS] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [error, setError] = React.useState('');

  const handleChangeOS = (event: SelectChangeEvent) => {
    setOS(event.target.value as string);
  };

  const handleChangeLanguage = (event: SelectChangeEvent) => {
    setLanguage(event.target.value as string);
  };

  const handleChangeError = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError(event.target.value as string);
  };

  const handleClick = () => {
    console.log(`${os}, ${language}, ${error}`);
  }

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          my: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Typography variant="h1" component="h1" gutterBottom>
          Search
        </Typography>
        <FormControl fullWidth sx={{ m: 1 }}>
          <InputLabel id="demo-simple-select-label">OS</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={os}
            label="OS"
            onChange={handleChangeOS}
          >
            <MenuItem value={"macOS"}>macOS</MenuItem>
            <MenuItem value={"Windows"}>Windows</MenuItem>
          </Select>
        </FormControl>
        <FormControl fullWidth sx={{ m: 1 }}>
          <InputLabel id="demo-simple-select-label">言語</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={language}
            label="言語"
            onChange={handleChangeLanguage}
          >
            <MenuItem value={"Python"}>Python</MenuItem>
            <MenuItem value={"JavaScript"}>JavaScript</MenuItem>
          </Select>
        </FormControl>
        <TextField
          id="outlined-multiline-static"
          label="エラー文"
          sx={{ m: 1 }}
          fullWidth
          multiline
          rows={10}
          value={error}
          onChange={handleChangeError}
        />
        <Box
          sx={{
            my: 1,
            display: 'flex',
            flexDirection: 'flex-end',
            justifyContent: 'flex-end',
            alignItems: 'flex-end'
          }}
        >
          <Button
            variant="contained"
            sx={{ minWidth: 200 }}
            onClick={handleClick}
          >検索</Button>
        </Box>
      </Box>
    </Container>
  );
}