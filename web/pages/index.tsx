import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import {
  Alert,
  Fade,
  IconButton,
  InputAdornment,
  OutlinedInput,
  Stack,
} from '@mui/material';
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
import CodeArea from '../src/components/codeArea';

export default function Search() {
  const [os, setOS] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [error, setError] = React.useState('');
  const [highlights, setHighlights] = React.useState([]);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [openSnackbar, setOpenSnackbar] = React.useState(false);
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
      body: JSON.stringify({ language: language, error_text: error }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data.result);
        setHighlights(data.result);
        const texts = data.result.map((x: { text: string }) => x.text) as [];
        const uniqueTexts = Array.from(new Set(texts).values());
        setSearchQuery(buildSearchQuery(uniqueTexts as []));
      })
      .catch((error) => {
        console.error('通信に失敗しました', error);
      });
  };

  const router = useRouter();

  const handleClickSearch = () => {
    console.log(`${os}, ${language}, ${error}`);
    fetch(`${BACKEND_ENDPOINT}/error_parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ language: language, error_text: error }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        const texts = data.result.map((x: { text: string }) => x.text) as [];
        const uniqueTexts = Array.from(new Set(texts).values());
        return router.push(
          `https://google.com/search?q=${uniqueTexts.join('+')}&lr=lang_ja`,
        );
      })
      .catch((error) => {
        console.error('通信に失敗しました', error);
      });
  };

  const handleClickCopy = () => {
    navigator.clipboard.writeText(searchQuery);
    setOpenSnackbar(true);
  };

  const handleMouseDownCopy = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  const handleCloseCopyAlert = () => {
    setOpenSnackbar(false);
  };

  const buildSearchQuery = (queryErrorContents: []) => {
    return [...queryErrorContents, 'in', language, 'on', os].join(' ');
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
      <Box>
        <Typography variant='h6' component='h2' gutterBottom>
          解析・生成結果
        </Typography>
        <Stack spacing={2} sx={{ mt: 2, mb: 8 }}>
          <FormControl>
            <InputLabel>検索文字列</InputLabel>
            <OutlinedInput
              inputProps={{ readOnly: true }}
              value={searchQuery}
              label='検索文字列'
              endAdornment={
                <InputAdornment position='end'>
                  <Box sx={{ zIndex: 'modal', pr: 1 }}>
                    <Fade in={openSnackbar}>
                      <Alert icon={false} severity='success'>
                        Copied
                      </Alert>
                    </Fade>
                  </Box>
                  <IconButton
                    aria-label='Click to copy'
                    onClick={handleClickCopy}
                    onMouseDown={handleMouseDownCopy}
                    onMouseOut={handleCloseCopyAlert}
                    edge='end'
                  >
                    <ContentCopyIcon />
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>
          <CodeArea errorText={error} highlights={highlights} />
        </Stack>
      </Box>
    </Container>
  );
}
