import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { Router as redu, useRouter } from 'next/router';
import * as React from 'react';

export default function Search() {
  const [os, setOS] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [error, setError] = React.useState('');
  const [queryErrorContents, setQueryErrorContents] = React.useState([]);
  const [isQueryBuildFinished, setQueryBuildFinished] = React.useState(false);
  const BACKEND_ENDPOINT = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT;

  const handleChangeOS = (event: SelectChangeEvent) => {
    setOS(event.target.value as string);
  };

  const handleChangeLanguage = (event: SelectChangeEvent) => {
    setLanguage(event.target.value as string);
  };

  const handleChangeError = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError(event.target.value as string);
  };

  const router = useRouter();

  const handleClick = () => {
    console.log(`${os}, ${language}, ${error}`);
    setQueryBuildFinished(true);
    fetch(`${BACKEND_ENDPOINT}/error_parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ language: language, error_text: error }),
    })
      .then((res) => res.json())
      .then(async (data) => {
        console.log(data);
        await setQueryErrorContents(
          data.result.map((x: { text: any }) => x.text) as [],
        );
        return router.push(
          `https://google.com/search?q=${queryErrorContents}&lr=lang_ja`,
        );
      });
  };

  return (
    <Container maxWidth='lg'>
      <Box
        sx={{
          my: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Typography variant='h1' component='h1' gutterBottom>
          Search
        </Typography>
        {isQueryBuildFinished && (
          <TextField
            fullWidth
            label='Sample Search Query'
            inputProps={{ readOnly: true }}
            value={[...queryErrorContents, 'in', language, 'on', os].join(' ')}
          ></TextField>
        )}
        <FormControl fullWidth sx={{ m: 1 }}>
          <InputLabel id='demo-simple-select-label'>OS</InputLabel>
          <Select
            labelId='demo-simple-select-label'
            id='demo-simple-select'
            value={os}
            label='OS'
            onChange={handleChangeOS}
          >
            <MenuItem value={'macOS'}>macOS</MenuItem>
            <MenuItem value={'Windows'}>Windows</MenuItem>
          </Select>
        </FormControl>
        <FormControl fullWidth sx={{ m: 1 }}>
          <InputLabel id='demo-simple-select-label'>言語</InputLabel>
          <Select
            labelId='demo-simple-select-label'
            id='demo-simple-select'
            value={language}
            label='言語'
            onChange={handleChangeLanguage}
          >
            <MenuItem value={'Python'}>Python</MenuItem>
            <MenuItem value={'JavaScript'}>JavaScript</MenuItem>
          </Select>
        </FormControl>
        <TextField
          id='outlined-multiline-static'
          label='エラー文'
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
            alignItems: 'flex-end',
          }}
        >
          <Button
            variant='contained'
            sx={{ minWidth: 200 }}
            onClick={handleClick}
          >
            検索
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
