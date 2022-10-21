import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import * as React from 'react';

// export default function CodeArea({ code, results }) {
export default function CodeArea() {
  const result = [
    {
      row_idx: 1,
      col_idxes: { start: 3, end: 8 },
    },
    {
      row_idx: 3,
      col_idxes: { start: 1, end: 4 },
    },
  ];

  const [errorText, setErrorText] = React.useState('');
  // const [highlightLines, sethighlightLines] = React.useState(Array<number>);

  const handleChangeError = (event: React.ChangeEvent<HTMLInputElement>) => {
    setErrorText(event.target.value as string);
    console.log(errorText, errorText.split('\n'));
  };

  const highlight = function (v: string, i: number): JSX.Element[] {
    if (result.some((v) => v.row_idx === i + 1)) {
      return result
        .filter((vf) => vf.row_idx === i + 1)
        .map((vm) => (
          <>
            <span>{v.slice(0, vm.col_idxes.start - 1)}</span>
            <span style={{ backgroundColor: 'lemonchiffon' }}>
              {v.slice(vm.col_idxes.start - 1, vm.col_idxes.end - 1)}
            </span>
            <span>{v.slice(vm.col_idxes.end - 1)}</span>
          </>
        ));
    } else {
      return [<span key={0}>{v}</span>];
    }
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
        {errorText.length > 0 && (
          <div
            style={{
              width: '100%',
              margin: '8px',
              padding: 0,
              paddingTop: 4,
              paddingBottom: 4,
              borderStyle: 'solid',
              borderWidth: 1,
              borderColor: 'rgba(0, 0, 0, 0.23)',
              borderRadius: 4,
            }}
          >
            <table
              style={{
                width: '100%',
                borderSpacing: 0,
                borderCollapse: 'collapse',
                fontFamily: 'monospace',
                fontSize: `0.9rem`,
              }}
            >
              <tbody>
                {errorText.split('\n').map((v, i) => (
                  <tr
                    key={i + 1}
                    style={{
                      padding: 0,
                    }}
                  >
                    <td
                      style={{
                        width: 40,
                        padding: 0,
                        paddingLeft: 8,
                        paddingRight: 8,
                        textAlign: 'right',
                        userSelect: 'none',
                        color: 'dimgray',
                      }}
                    >
                      {i + 1}
                    </td>
                    <td
                      style={{
                        padding: 0,
                        paddingLeft: 8,
                        paddingRight: 8,
                        whiteSpace: 'pre',
                      }}
                    >
                      {highlight(v, i)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Box>
    </Container>
  );
}
