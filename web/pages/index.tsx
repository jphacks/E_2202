import { Stack } from '@mui/material';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import * as React from 'react';

export default function Search() {
  const [os, setOS] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [error, setError] = React.useState('');
  const [queryErrorContents, setQueryErrorContents] = React.useState([]);
  const [analyzedError, setAnalyzedError] = React.useState('');
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

  const handleClickAnalyze = () => {
    console.log(`${os}, ${language}, ${error}`);
    fetch(`${BACKEND_ENDPOINT}/error_parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ error_text: error }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setQueryErrorContents(data.result as []);
        setAnalyzedError(error);
      })
      .catch((error) => {
        console.error('通信に失敗しました', error);
      });
  };

  const handleClickSearch = () => {
    console.log(`${os}, ${language}, ${error}`);
    fetch(`${BACKEND_ENDPOINT}/error_parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ error_text: error }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setQueryErrorContents(data.result as []);
      })
      .catch((error) => {
        console.error('通信に失敗しました', error);
      });
  };

  return (
    <Container maxWidth='lg'>
      <Box
        sx={{
          my: 4,
          pb: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          borderBottom: 1,
          borderColor: 'grey.500',
        }}
      >
        <Typography variant='h1' gutterBottom>
          Search
        </Typography>
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
        <Stack direction='row' spacing={8} sx={{ m: 4 }}>
          <Button
            variant='contained'
            sx={{ width: 200, height: 50 }}
            onClick={handleClickAnalyze}
          >
            解析・生成
          </Button>
          <Button
            variant='contained'
            sx={{ width: 200, height: 50 }}
            onClick={handleClickSearch}
          >
            検索
          </Button>
        </Stack>
      </Box>
      <Typography variant='h6' component='h2' gutterBottom>
        解析・生成結果
      </Typography>
      <Stack spacing={2} sx={{ mt: 2, mb: 8 }}>
        <TextField
          fullWidth
          label='Sample Search Query'
          inputProps={{ readOnly: true }}
          value={[...queryErrorContents, 'in', language, 'on', os].join(' ')}
        ></TextField>
        <TextField
          label='エラー文'
          fullWidth
          multiline
          rows={10}
          inputProps={{ readOnly: true }}
          value={analyzedError}
          defaultValue=' '
        />
      </Stack>
    </Container>
  );
}
