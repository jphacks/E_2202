import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import * as React from 'react';
import CodeArea from '../src/components/codeArea';

export default function CodeAreaDemo() {
  const result = [
    {
      row_idx: 1,
      col_idxes: { start: 3, end: 8 },
      text: '',
      type: '',
    },
    {
      row_idx: 3,
      col_idxes: { start: 1, end: 4 },
      text: '',
      type: '',
    },
  ];

  const [errorText, setErrorText] = React.useState('');

  const handleChangeError = (event: React.ChangeEvent<HTMLInputElement>) => {
    setErrorText(event.target.value as string);
    console.log(errorText, errorText.split('\n'));
  };

  return (
    <Container maxWidth='lg'>
      <Box>
        <TextField
          id='outlined-multiline-static'
          label='エラー文'
          sx={{ m: 1 }}
          fullWidth
          multiline
          rows={10}
          value={errorText}
          onChange={handleChangeError}
        />
        <CodeArea errorText={errorText} highlights={result} />
      </Box>
    </Container>
  );
}
